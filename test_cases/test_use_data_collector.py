from PySide6.QtCore import Signal, QByteArray, QObject

from modules.use_data_collector import DataCollectorClass
from modules.db_functions import DbClass
from modules.bluetooth_serial_communication import BtSerialComm

import pytest, pytestqt

class FakeSocket(QObject):
    
    readyRead = Signal()
    
    def __init__(self):
        super().__init__()

        self.data = None
        self.sentMessage = None

    def readAll(self):
        if self.data:
            return QByteArray(self.data)
    
    def isOpen(self):
        return True

    def write(self,message):
        self.sentMessage = message
        
class TestUseDataCollector:

    def setup_method(self, method):
        self.fake_socket = FakeSocket()
        self.bt_class = BtSerialComm()
        self.bt_class.bt_socket = self.fake_socket
        self.db_class = DbClass()
        self.data_collector_class = DataCollectorClass(self.db_class, self.bt_class, logModel = None)

    def test_start_checker_success(self):
        self.data_collector_class.start_watch = True

        assert self.fake_socket.sentMessage == b"*L1"