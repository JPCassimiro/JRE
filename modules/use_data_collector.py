from PySide6.QtCore import QObject, QTimer, Signal

from modules.log_class import logger

import time
class DataCollectorClass(QObject):
    errorOcurred = Signal(bool)

    def __init__(self, dbHandleClass, SerialCommClass, btSerialHandle, logModel):
        super().__init__()
        
        #variable setup
        self._start_watch = False
        self.message_buffer = [[],[]]
        self.current_user_index = None
        self.current_session_index = None
        
        self.logModel = logModel
        
        #module setup
        self.timer = QTimer()
        self.dbHandleClass = dbHandleClass
        self.serialHandleClass = SerialCommClass
        self.btSerialHandle = btSerialHandle

        #connections setup
        self.timer.timeout.connect(self.timeout_handle)
    
    #value watcher setup
    #when atributed will check value
    #true = start
    @property
    def start_watch(self):
        return self._start_watch
    
    @start_watch.setter
    def start_watch(self,val):
        self._start_watch = val
        self.start_checker()
        
    def start_checker(self):
        try:
            if self._start_watch != False:
                self.start_data_collection(2500)
                self.send_serial_message("*L1")
                time.sleep(0.5)#attemps to garantee that the response from L1 will be handled on the regular message listner
                self.btSerialHandle.swap_message_listner(1)
                # self.serialHandleClass.swap_message_listner(1)
                self.btSerialHandle.mesReceivedSignal.connect(self.message_received_handler)
                # self.btSerialHandle.fake_stat_data()
                # self.serialHandleClass.mesReceivedSignal.connect(self.message_received_handler)
            else:
                self.timer.stop()
                self.btSerialHandle.swap_message_listner(0)
                # self.serialHandleClass.swap_message_listner(0)
                self.btSerialHandle.mesReceivedSignal.disconnect(self.message_received_handler)
                # self.serialHandleClass.mesReceivedSignal.disconnect(self.message_received_handler)
                self.timeout_handle()
                self.send_serial_message("*L0")
        except Exception as e:
            logger.error(f"Erro ao alterar o processo de coleta: {e}")
            self.message_buffer = [[],[]]
            self.errorOcurred.emit(True)

    def generate_query(self,inhale,exhale):
        try:
            q = "insert into use_data (session_id,action,pressure) values (?,?,?);"
            if self.current_session_index:
                data = []
                #2 same size arrays with x items
                for i,v in enumerate(inhale):
                    if int(inhale[i]) > 0:
                        data.append((self.current_session_index, 'inhale', int(inhale[i])))
                    if int(exhale[i]) > 0:
                        data.append((self.current_session_index, 'exhale', int(exhale[i])))
                return q,data
            else:
                logger.error(f"Não pode gerar um query para estatisticas de uso, paciente não selecionado")
        except Exception as e:
            logger.error(f"Erro durante a geração da query para entrada de dados no BD: {e}")
            self.message_buffer = [[],[]]
            self.errorOcurred.emit(True)
            
    def start_data_collection(self,ms):
        self.timer.start(ms)
        
    # start the process to send messages to the database
    def timeout_handle(self):
        try:
            if any(self.message_buffer):
                exhale_array = self.message_buffer[0]
                inhale_array = self.message_buffer[1]
                q,data = self.generate_query(inhale_array,exhale_array)
                if q != "" and data:
                    self.insert_data(q,data)
                    self.message_buffer = [[],[]]
            else:
                logger.debug(f"Message buffer vazio: {self.message_buffer}")
        except Exception as e:
            logger.error(f"Erro ao iniciar o processo de padronização de leituras: {e}")
            self.message_buffer = [[],[]]
            self.errorOcurred.emit(True)

    def insert_data(self,q,data):
        res = self.dbHandleClass.execute_multiple_queries(q,data)
        if res:
            logger.debug(f"estatisticas de uso inseridos na tabela: {res[0][0]}")
        
    def stop_data_collection(self):
        self.start_watch = False

    #appends messages on the buffer
    #*Ixxxyyy format every time
    #splits message on each array
    #each message has 3 digits
    def message_received_handler(self,message):
        logger.debug(f"DataCollectorClass message_received_handler message:{message}")
        self.logModel.append_log(message)
        for m in message:
            messages = [m[2:5],m[5:]] 
            for i, msg in enumerate(messages):
                self.message_buffer[i].append(messages[i])
                logger.debug(f"Mensagem adicionada ao buffer no indice {i}: {messages[i]}")
                logger.debug(f"Pressões recebidas - Sopro: {int(messages[0])/10} kPa - Sucção: {int(messages[1])/10} kPa")
                
    def send_serial_message(self,message):
        self.btSerialHandle.open_port()
        # self.serialHandleClass.open_port()
        self.btSerialHandle.send_message(message)
        # self.serialHandleClass.send_message(message)


            
