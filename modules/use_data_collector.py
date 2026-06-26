from PySide6.QtCore import QObject, QTimer, Signal

from shared_ui_modules.modules.log_class import logger

from shared_ui_modules.modules.use_data_colector import SharedDataCollectorClass

from modules.db_functions import DbClass
from modules.bluetooth_serial_communication import BtSerialComm
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

import time
class DataCollectorClass(SharedDataCollectorClass):
    errorOcurred = Signal(bool)

    def __init__(self, dbHandleClass: DbClass, btSerialHandle: BtSerialComm, logModel: SharedLogModel):
        super().__init__(dbHandleClass, btSerialHandle, logModel)
        
        #variable setup
        self._start_watch = False
        self.message_buffer = [[],[]]
        self.current_user_index = None
        self.current_session_index = None
        
        self.logModel = logModel
        
        #module setup
        self.timer = QTimer()
        self.dbHandleClass = dbHandleClass
        self.btSerialHandle = btSerialHandle

        #connections setup
        self.timer.timeout.connect(self.timeout_handle)

        self.initilize_module()

    def get_message_buffer(self):
        return [[],[]]
    
    def generate_query(self,inhale,exhale):
        try:
            if self.current_session_index is None:
                raise Exception(f"null current_session: {self.current_session_index}")

            q = "insert into use_data (session_id,action,pressure) values (?,?,?);"
            data = []
            #2 same size arrays with x items
            for i,v in enumerate(inhale):
                if int(inhale[i]) > 0:
                    data.append((self.current_session_index, 'inhale', int(inhale[i])))
                if int(exhale[i]) > 0:
                    data.append((self.current_session_index, 'exhale', int(exhale[i])))
            return q,data
        except Exception as e:
            logger.error(f"DataCollectorClass generate_query error: {e}")
            self.message_buffer = [[],[]]
            self.errorOcurred.emit(True)
        
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
            logger.error(f"DataCollectorClass timeout_handle error: {e}")
            self.message_buffer = [[],[]]
            self.errorOcurred.emit(True)

    #appends messages on the buffer
    #*Ixxxyyy format every time
    #splits message on each array
    #each message has 3 digits
    def message_received_handler(self,message):
        try:
            logger.debug(f"DataCollectorClass message_received_handler message:{message}")
            self.logModel.append_log(message)
            for m in message:
                messages = [m[2:5],m[5:]] 
                for i, msg in enumerate(messages):
                    self.message_buffer[i].append(messages[i])
                    logger.debug(f"Mensagem adicionada ao buffer no indice {i}: {messages[i]}")
                    logger.debug(f"Pressões recebidas - Sopro: {int(messages[0])/10} kPa - Sucção: {int(messages[1])/10} kPa")
        except Exception as e:
            logger.error(f"DataCollectorClass message_received_handler error: {e}")