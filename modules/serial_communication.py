import wmi
import re

from modules.log_class import logger

from PySide6.QtCore import Signal, QObject, QTimer
from PySide6.QtSerialPort import QSerialPort
from PySide6.QtCore import QIODevice

from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID, ID_MODEL_FROM_DATABASE, ID_VENDOR_FROM_DATABASE, DEVNAME

baud_rate = 600

#! port opening needs to be revised 
#! device listner would help solve this

class SerialCommClass(QObject):
    
    port_finish = Signal()
    port_error = Signal()
    mesReceivedSignal = Signal(object)
    
    def __init__(self, parent=None):
        super().__init__()
        
        #port setup
        #baud rate
        #port
        #timeout
        #device mac addrs
        self.ser = QSerialPort()
        self.ser.setBaudRate(baud_rate)
        self.message_buffer = ""
        self.use_data_buffer = ""
        self.device_mac_addr = ''

        self.use_data_regex = r"\*I\d{12}"

        self.c = wmi.WMI()
        self.usb_monitor = USBMonitor()
                
        self.timer = QTimer()
        self.pause_var = False

        #for testing
        # self.device_mac_addr = "d48afc9d936a"
        # self.ser.setPortName(r"\\.\COM19")

        #when a new char message is ready to be read on the serial port
        self.ser.readyRead.connect(self.recieve_message)
        self.ser.errorOccurred.connect(self.handle_serial_error)
        self.timer.timeout.connect(self.handle_timeout)

        # self.usb_monitor_start()

    #toggles port state
    def alter_port_state(self):
        if self.ser.isOpen():
            self.ser.close()
        else:
            self.ser.open()
        
    # if port not open
    def open_port(self):
        if not self.ser.isOpen():
           if not self.ser.open(QIODevice.ReadWrite):
               logger.error(f"Erro ao abrir porta serial: {self.ser.errorString()}")

    #gets message from model class and writes it
    def send_message(self, message):
        encodedMessage = message.encode('utf-8')
        self.ser.write(encodedMessage)
        
    #gets message, decodes, sends signal
    def recieve_message(self):
        message_substrings = []#mesages to be sent
        data = self.ser.readAll()#these messages can be recieved in any way at any time, so it can be split or concateneted
        dataStr = data.toStdString()
        self.message_buffer += dataStr
        print(f"recive_message:{self.message_buffer}")
        while "N" in self.message_buffer or "A" in self.message_buffer:
            last_index = 0
            for i, c in enumerate(self.message_buffer):#get the substring up to the limiter
                if c == "A" or c == "N":
                    message_substrings.append(self.message_buffer[:i+1])
                    last_index = i
                    break
            self.message_buffer = self.message_buffer[last_index+1:]
        for m in message_substrings:
            self.mesReceivedSignal.emit(m)
            logger.debug(f"Mensagem recebida: {m}")
             
    #receives sensor readings
    def recieve_use_data_message(self):
        if self.pause_var != True:
            messages = []
            data = self.ser.readAll()
            dataStr = data.toStdString()
            self.use_data_buffer += dataStr
            matches = list(re.finditer(self.use_data_regex,self.use_data_buffer))
            print(f"recieve_use_data_message self.use_data_buffer:{self.use_data_buffer}\ndataStr:{dataStr}\nmatches:{matches}")
            if matches:
                last_match = matches[-1]
                start, end = last_match.span()
                self.use_data_buffer = self.message_buffer[end+1:]
                self.start_timer()
            for m in matches:
                messages.append(m.group())
                logger.debug(f"Mensagem recebida: {m.group()}")
            if messages:
                self.mesReceivedSignal.emit(messages)
                    
    #logs error on serial
    def handle_serial_error(self,err):
        logger.error(err)        
        
    #ports that are >=10 must be inputed this way due to a windows quirk of finding ports, Qt does not automatically deals with this like pyserial
    def port_name_normalization(self,portName):
        portNumber = int(portName[3:])
        if portNumber >= 10:
            portName = r"\\.\{}".format(portName)
        return portName
    
    def find_port(self):
        try:
            logger.debug("find_port attempting to find port name")
            if self.device_mac_addr != "":
                logger.debug(f"find_port self.device_mac_addr:{self.device_mac_addr}")
                com_devices = self.c.query("SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%(COM%'")
                logger.debug(f"find_port com_devices:{com_devices}")
                for com_device in com_devices:
                    if self.device_mac_addr in str(com_device.deviceID).lower():#found com port 
                        logger.debug("find_port found com port")
                        start =  str(com_device.Name).lower().find("(com")
                        end =  str(com_device.Name).lower().find(")",start)
                        self.ser.setPortName(self.port_name_normalization(str(com_device.Name[start+1:end]).lower()))
                        self.port_finish.emit()
                        logger.debug(f"find_port self.ser.portName():{self.ser.portName()}")
            else:
                logger.error("Encontre o endereço MAC primeiro")
                self.port_error.emit()

        except Exception as e:
                logger.error("Erro no processo de obter porta COM")
                self.port_error.emit()

    def swap_message_listner(self,op = 0):
        self.ser.readyRead.disconnect()
        if op == 0:#default
            self.ser.readyRead.connect(self.recieve_message)
        elif op == 1:#use_data_collector
            self.ser.readyRead.connect(self.recieve_use_data_message)
            
    #on sucessfull read stop reading for 1 sec, deals with multiple messages of same value
    def start_timer(self):
        self.timer.start(1000)
        self.pause_var = True
        
    def handle_timeout(self):
        self.pause_var = False
        self.ser.clear(QSerialPort.Input)

    def clear_serial_info(self):
        self.device_mac_addr = None#clear device info from serialHandleClass
        self.ser.port = ''
        if self.ser.isOpen():
            self.ser.close()
        self.ser.setPortName('')
        
    def usb_monitor_start(self):
        self.usb_monitor.start_monitoring(on_connect = self.on_usb_device_connect, on_disconnect = None)
        
    def on_usb_device_connect(self,device_id: str, device_info: dict):
        logger.debug(f"device_info: {device_info[ID_MODEL],device_info[ID_MODEL_ID],device_info[ID_VENDOR_ID],device_info[ID_MODEL_FROM_DATABASE], device_info[ID_VENDOR_FROM_DATABASE], device_info[DEVNAME]}")
        logger.debug(f"device_id: {device_id}")
        
    # def find_device_by_port(self):
        