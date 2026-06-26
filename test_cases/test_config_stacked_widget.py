from PySide6.QtCore import QObject, QByteArray, Signal
from PySide6.QtTest import QSignalSpy

from modules.bluetooth_serial_communication import BtSerialComm
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

from ui.model.stacked_widget_screens.config_widget_model import ConfigWidgetModel

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
    
class TestConfigStackedWidget:
    
    def setup_method(self,method):
        self.fake_socket = FakeSocket()
        self.bt_serial_class = BtSerialComm()
        self.bt_serial_class.bt_socket = self.fake_socket
        self.logModel = SharedLogModel(self.bt_serial_class)
        self.config_widget = ConfigWidgetModel(LogModel=self.logModel, btSerialHandle=self.bt_serial_class)

    def test_confirm_message_generator_success(self,qtbot):
        self.config_widget.p_value = (0,100)
        self.config_widget.p_value = (1,200)
        self.config_widget.param_select = {
            "key_1":"A",
            "key_2":"B",
            "repeat_key":True,
            "duration":9
        }

        messages, bindingArray = self.config_widget.confirm_messages_generator()

        assert len(messages) == 8
        assert messages[0] == "*M1100"
        assert messages[1] == "*BA"
        assert messages[2] == messages[6] == "*R1"
        assert messages[3] == messages[7] == "*T9"
        assert messages[4] == "*M2200"
        assert messages[5] == "*UB"

        assert len(bindingArray) == 2        
        assert bindingArray[0] == {
            "repeat": True,
            "duration":9,
            "key": "A",
            "pressure": 100,
            "action": 1
        }
        assert bindingArray[1] == {
            "repeat": True,
            "duration":9,
            "key": "B",
            "pressure": 200,
            "action": 2
        }
        
    def test_slider_value_change_success(self,qtbot):
        qtbot.addWidget(self.config_widget)
        
        for slider in self.config_widget.slider_array:
            slider.slider.setValue(100)

        assert self.config_widget.p_value[0] == self.config_widget.p_value[1] == 100
        assert self.config_widget.exhaleSelectButton.isEnabled() == self.config_widget.exhaleSelectButton.isEnabled() == True 

        self.config_widget.slider_array[0].slider.setValue(0)

        assert self.config_widget.p_value[0] == 0 
        assert self.config_widget.exhaleSelectButton.isEnabled() == False

        self.config_widget.slider_array[1].slider.setValue(0)

        assert self.config_widget.p_value[1] == 0 
        assert self.config_widget.inhaleSelectButton.isEnabled() == False

    def test_key_duration_repeat_selection_success(self,qtbot,monkeypatch):
        #add both stacked screen widget and key select modal
        qtbot.addWidget(self.config_widget)
        qtbot.addWidget(self.config_widget.key_select_modal)

        #patch the key_select_modal 
        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.config_widget.key_select_modal,
            "exec",
            lambda: None
        )
        
        #change slider value
        #press corresponding button
        #send desired key
        #assert values
        
        self.config_widget.slider_array[0].slider.setValue(50)
        self.config_widget.exhaleSelectButton.click()
        qtbot.keyPress(self.config_widget.key_select_modal,"A")

        assert self.config_widget.key_select_modal.keyDisplayer.text().upper() == "A"

        assert self.config_widget.key_select_modal.selected_key == "A"

        self.config_widget.key_select_modal.buttonBox.buttons()[0].click()

        assert self.config_widget.p_value[0] == 50
        assert self.config_widget.param_select["key_1"] == "A"
        
        self.config_widget.slider_array[1].slider.setValue(85)
        self.config_widget.inhaleSelectButton.click()
        qtbot.keyPress(self.config_widget.key_select_modal,"B")

        assert self.config_widget.key_select_modal.keyDisplayer.text().upper() == "B"
        assert self.config_widget.key_select_modal.selected_key == "B"

        self.config_widget.key_select_modal.buttonBox.buttons()[0].click()

        assert self.config_widget.p_value[1] == 85
        assert self.config_widget.param_select["key_2"] == "B"

        self.config_widget.repeatOnButton.click()

        assert self.config_widget.repeatOnButton.isChecked() == True
        assert self.config_widget.param_select["repeat_key"] == True

        self.config_widget.durationSlider.setValue(9)

        assert self.config_widget.durationSlider.value() == 9
        assert self.config_widget.param_select["duration"] == 9

        #use reset button for both sliders
        #check if param_select is back to default
        #check if buttons are enabled

        self.config_widget.resetExhalePressureValueButton.click()

        assert self.config_widget.slider_array[0].slider.value() == 0
        assert self.config_widget.p_value[0] == 0
        assert self.config_widget.param_select["key_1"] == None
        assert self.config_widget.exhaleSelectButton.isEnabled() == False

        self.config_widget.resetInhalePressureValueButton.click()

        assert self.config_widget.slider_array[1].slider.value() == 0
        assert self.config_widget.p_value[1] == 0
        assert self.config_widget.param_select["key_2"] == None
        assert self.config_widget.inhaleSelectButton.isEnabled() == False

        assert self.config_widget.param_select["duration"] == 0
        assert self.config_widget.param_select["repeat_key"] == False
        assert self.config_widget.durationSlider.isEnabled() == False
        assert self.config_widget.repeatOnButton.isEnabled() == False
        assert self.config_widget.repeatOffButton.isEnabled() == False

    def test_reset_screen_variables_success(self,qtbot,monkeypatch):
        #add both stacked screen widget and key select modal
        qtbot.addWidget(self.config_widget)
        qtbot.addWidget(self.config_widget.key_select_modal)

        #patch the key_select_modal 
        #change the exec() function to none so the modal dosent get triggered and crashes the test
        monkeypatch.setattr(
            self.config_widget.key_select_modal,
            "exec",
            lambda: None
        )

        for slider in self.config_widget.slider_array:
            slider.slider.setValue(50)

        self.config_widget.exhaleSelectButton.click()
        qtbot.keyPress(self.config_widget.key_select_modal,"A")
        self.config_widget.key_select_modal.buttonBox.buttons()[0].click()
        
        self.config_widget.inhaleSelectButton.click()
        qtbot.keyPress(self.config_widget.key_select_modal,"B")
        self.config_widget.key_select_modal.buttonBox.buttons()[0].click()

        self.config_widget.repeatOnButton.click()
        self.config_widget.durationSlider.setValue(9)

        self.config_widget.p_value = (0,0)
        self.config_widget.p_value = (1,0)

        assert self.config_widget.param_select == {
            "key_1":None,
            "key_2":None,
            "repeat_key":False,
            "duration":0
        }
        
        assert self.config_widget.durationSlider.isEnabled() == False
        assert self.config_widget.repeatOnButton.isEnabled() == False
        assert self.config_widget.repeatOffButton.isEnabled() == False
        assert self.config_widget.exhaleSelectButton.isEnabled() == False
        assert self.config_widget.inhaleSelectButton.isEnabled() == False
        
    def test_assing_card_value_success(self,qtbot):
        duration = 9
        action = 1
        key = "A"
        repeat = True
        pressure = 100
        self.config_widget.assing_card_values({
            "repeat": repeat,
            "duration":duration,
            "key": key,
            "pressure": pressure,
            "action": action
        })
        
        assert self.config_widget.slider_array[action-1].slider.value() == pressure
        assert self.config_widget.repeatOnButton.isChecked() == repeat
        assert self.config_widget.param_select[f"key_{action}"] == key
        assert self.config_widget.durationSlider.value() == duration
        if action-1 == 0:
            assert self.config_widget.exhaleSelectButton.text().upper() == key
        else:
            assert self.config_widget.inhaleSelectButton.text().upper() == key
        