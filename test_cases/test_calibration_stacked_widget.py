from ui.model.stacked_widget_screens.calibration_widget_model import CalibrationWidgetModel

from modules.bluetooth_serial_communication import BtSerialComm
from shared_ui_modules.modules.bluetooth_comunication import BluetoothCommClass
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

from PySide6.QtCore import QObject, QByteArray, Signal
from PySide6.QtTest import QSignalSpy

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

class TestCallibrationStackedWidget:

    def setup_method(self,method):
        self.fake_socket = FakeSocket()
        self.bt_serial_class = BtSerialComm()
        self.bt_serial_class.bt_socket = self.fake_socket
        self.logModel = SharedLogModel(self.bt_serial_class)
        self.cali_widget = CalibrationWidgetModel(logModel=self.logModel, btSerialhandle=self.bt_serial_class)

    def test_restart_calibration_success(self, qtbot):
        #setup qtbot
        qtbot.addWidget(self.cali_widget)
        #now qtbot has access to all elements from the widget
        
        self.cali_widget.restartButton.click()

        #check variables
        #success cases
        assert self.cali_widget.step_1_pressure == [0] 
        assert self.cali_widget.step_2_pressure == [0] 
        assert self.cali_widget.timeout_counter == 0 
        assert self.cali_widget.calibration_step == 0 
        
        #check visual elements
        #success cases
        assert self.cali_widget.stackedWidget.currentIndex() == 0
        assert self.cali_widget.instructionText.text() == self.cali_widget.string_list_instruction[self.cali_widget.calibration_step]
        assert self.cali_widget.imgLabel.maximumWidth() == self.cali_widget.image_data[self.cali_widget.calibration_step][1]
        assert self.cali_widget.imgLabel.maximumHeight() == self.cali_widget.image_data[self.cali_widget.calibration_step][2]
        assert self.cali_widget.startButton.isEnabled() == True
        # assert self.cali_widget.instructionText.isVisible() == True
        # assert self.cali_widget.imgLabel.isVisible() == True
        
    def test_update_screen_step_2_success(self,qtbot):
        #setup qtbot
        qtbot.addWidget(self.cali_widget)

        self.cali_widget.calibration_step = 1

        self.cali_widget.update_instruction_ui()
        
        assert self.cali_widget.instructionText.text() == self.cali_widget.string_list_instruction[self.cali_widget.calibration_step]
        assert self.cali_widget.imgLabel.maximumWidth() == self.cali_widget.image_data[self.cali_widget.calibration_step][1]
        assert self.cali_widget.imgLabel.maximumHeight() == self.cali_widget.image_data[self.cali_widget.calibration_step][2]
        
    def test_cancel_button_success(self,qtbot):
        #setup qtbot
        qtbot.addWidget(self.cali_widget)
        sideMenuDisable_sig_spy = QSignalSpy(self.cali_widget.sideMenuDisableSignal)

        self.cali_widget.startButton.click()
        self.cali_widget.cancelButton.click()

        assert self.cali_widget.timeout_counter == 0
        assert self.cali_widget.cancelButton.isEnabled() == False
        assert self.cali_widget.restartButton.isEnabled() == False
        assert self.cali_widget.startButton.isEnabled() == True
        assert self.cali_widget.error_flag == False
        assert sideMenuDisable_sig_spy.count() != 0

    def test_start_button_success(self, qtbot):
        #setup qtbot
        qtbot.addWidget(self.cali_widget)
        sideMenuDisable_sig_spy = QSignalSpy(self.cali_widget.sideMenuDisableSignal)
        
        self.cali_widget.startButton.click()

        assert self.cali_widget.startButton.isEnabled() == False
        assert self.cali_widget.restartButton.isEnabled() == False
        assert self.cali_widget.cancelButton.isEnabled() == True
        assert self.cali_widget.timer.isActive() == True
        assert sideMenuDisable_sig_spy.count != 0
        assert self.cali_widget.error_flag == False 
        
    def test_present_results_success(self, qtbot):
        #setup qtbot
        qtbot.addWidget(self.cali_widget)

        self.cali_widget.step_1_pressure = [123]
        self.cali_widget.step_2_pressure = [321]

        self.cali_widget.present_results()
        res = self.cali_widget.get_max_pressure_values()

        assert self.cali_widget.stackedWidget.currentIndex() == 1
        assert self.cali_widget.startButton.isEnabled() == False
        assert res == [123, 321]