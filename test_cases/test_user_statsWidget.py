from PySide6.QtCore import QObject, QByteArray, Signal, Qt
from PySide6.QtTest import QSignalSpy

from ui.model.stacked_widget_screens.user_stats_model import UserStatsModel

from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm
from modules.db_functions import DbClass

import pytestqt
from unittest.mock import Mock 

class FakeDb(DbClass):
    
    def get_db_name(self):
        return "test_db"

class FakeSocket(QObject):
    
    readyRead = Signal()
    
    def __init__(self):
        super().__init__()

        self.data = None

    def readAll(self):
        if self.data:
            return QByteArray(self.data)
    
    def isOpen(self):
        return True

class FakeLogClass(QObject):
    
    def append_log(self,message):
        print(message)

class TestUserStats:

    def setup_method(self,method):
        self.serialBthandle = SharedBtSerialComm()
        self.serialBthandle.bt_socket = FakeSocket()
        self.fake_log = FakeLogClass()
        self.db_class = FakeDb()
        
        self.user_stats = UserStatsModel(btSerialHandle=self.serialBthandle,LogModel=self.fake_log,dbHandleClass=self.db_class)
        for s in ["delete from therapist;","delete from patient;","delete from session;","delete from use_data;","delete from bindings;","delete from game_profile;","""insert into patient (id, name, details, image_path) values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');""","""insert into therapist (id, name, details, image_path) values (1, 'terapeuta padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"""]:
            self.db_class.execute_single_query(s)
        
    def test_create_session_success(self,qtbot,monkeypatch):
        qtbot.addWidget(self.user_stats)
        
        self.user_stats.assing_user(1,"Paciente padrão")
        
        qtbot.mouseClick(
            self.user_stats.newSessionButton,
            Qt.LeftButton,
            pos = self.user_stats.newSessionButton.rect().center()
        )

        assert self.user_stats.sessionComboBox.count() == 1

    def test_delete_session_success(self,qtbot,monkeypatch):
        qtbot.addWidget(self.user_stats)
        
        self.user_stats.assing_user(1,"Paciente padrão")

        qtbot.mouseClick(
            self.user_stats.newSessionButton,
            Qt.LeftButton,
            pos = self.user_stats.newSessionButton.rect().center()
        )

        assert self.user_stats.sessionComboBox.count() == 1

        monkeypatch.setattr(
            self.user_stats,
            "show_deletion_dialog",
            lambda: self.user_stats.deletion_dialog_accept()
        )

        qtbot.mouseClick(
            self.user_stats.deleteSessionButton,
            Qt.LeftButton,
            pos = self.user_stats.deleteSessionButton.rect().center()
        )
        
        assert self.user_stats.sessionComboBox.count() == 0
        
    def test_export_as_image_success(self,qtbot,monkeypatch):
        qtbot.addWidget(self.user_stats)

        self.user_stats.assing_user(1,"Paciente padrão")
        
        qtbot.mouseClick(
            self.user_stats.newSessionButton,
            Qt.LeftButton,
            pos = self.user_stats.newSessionButton.rect().center()
        )
        
        end_export_mock = Mock()

        monkeypatch.setattr(
            self.user_stats,
            "end_export_handle",
            end_export_mock
        )

        qtbot.mouseClick(
            self.user_stats.exportSessionImageButton,
            Qt.LeftButton,
            pos = self.user_stats.exportSessionImageButton.rect().center()
        )

        print(f"end_export_mock.call_args : {end_export_mock.call_args}")
        
        assert str(end_export_mock.call_args.args[0])== 'dados_de_uso\\paciente_1_paciente_padrao'

    def test_export_as_csv_success(self,qtbot,monkeypatch):
        qtbot.addWidget(self.user_stats)
            
        self.user_stats.assing_user(1,"Paciente padrão")
        
        qtbot.mouseClick(
            self.user_stats.newSessionButton,
            Qt.LeftButton,
            pos = self.user_stats.newSessionButton.rect().center()
        )

        end_export_mock = Mock()

        monkeypatch.setattr(
            self.user_stats,
            "end_export_handle",
            end_export_mock
        )
        
        sigSpy_csv_end = QSignalSpy(self.user_stats.csvWriter.exportEnd)

        qtbot.mouseClick(
            self.user_stats.exportSessionCSVButton,
            Qt.LeftButton,
            pos = self.user_stats.exportSessionCSVButton.rect().center()
        )

        assert str(end_export_mock.call_args.args[0])== 'dados_de_uso\\paciente_1_paciente_padrao'

        assert sigSpy_csv_end.count() == 1