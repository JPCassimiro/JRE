from ui.views.config_widget_ui import Ui_configForm

from ui.model.dialogs.key_select_model import KeySelectModel
from ui.model.components.end_config_model import EndConfigModel
from ui.model.custom_widgets.custom_slider_model import CustomSliderModel

from modules.log_class import logger
from modules.json_writer import JsonWriterClass

from PySide6.QtWidgets import QWidget, QRadioButton, QMessageBox, QSpacerItem, QSizePolicy
from PySide6.QtCore import QRect, Qt, QCoreApplication, QEvent

param_select_base_val = {
    "repeat_key":False,
    "key":None,
    "duration":0
}


class ConfigWidgetModel(QWidget):
    def __init__(self,serialHandleClass, btSerialHandle, LogModel):
        super().__init__()

        self.string_list_dialog = [
            "Erro",   
            "Escolha a tecla a ser emulada"            
        ]        

        self.string_list_components = [
            QCoreApplication.translate("ConfigJoystickComponents", "Clique para selecionar")
        ]        

        #ui setup
        self.ui = Ui_configForm()
        self.ui.setupUi(self)

        self.key_select_modal = KeySelectModel()
        self.end_modal = EndConfigModel()
        self.serialHandleClass = serialHandleClass
        self.logModel = LogModel
        self.btSerialHandle = btSerialHandle
        self.jsonWriter = JsonWriterClass()

        #variables setup
        self._selected_action = None #using the slider will change this, 0 on both = None, exhale = 1, inhale = 2 
        self.param_select = param_select_base_val.copy()
        self.p_value = 0
        self.current_user = None
        
        self.exhaleSlider = CustomSliderModel()
        self.inhaleSlider = CustomSliderModel()
        
        self.slider_array = [
            self.exhaleSlider,
            self.inhaleSlider
        ]
        
        #optionsContainer elements
        self.repeatOffButton = self.ui.repeatOffButton
        self.repeatOnButton = self.ui.repeatOnButton

        #duration slider
        self.durationSlider = self.ui.durationSlider

        #spacers
        self.inhaleSpacer = QSpacerItem(20, 489, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.exhaleSpacer = QSpacerItem(20, 489, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        #buttons
        self.inhaleSelectButton = self.ui.inhaleSelectButton
        self.exhaleSelectButton = self.ui.exhaleSelectButton
        self.confirmButton = self.ui.confirmButton

        self.inhaleSelectButton.setEnabled(False)
        self.exhaleSelectButton.setEnabled(False)

        self.exhaleSlider.slider.setProperty("index",1)
        self.inhaleSlider.slider.setProperty("index",2)

        #add sliders to screen
        self.ui.exhaleSliderContainer.layout().addWidget(self.exhaleSlider)
        self.ui.exhaleSliderContainer.layout().addSpacerItem(self.exhaleSpacer)
        
        self.ui.inhaleSliderContainer.layout().addWidget(self.inhaleSlider)
        self.ui.inhaleSliderContainer.layout().addSpacerItem(self.inhaleSpacer)
        
        #connections
        for slider in self.slider_array:
            slider.setEnabled(True)
            slider.slider.valueChanged.connect(self.pressure_slider_value_change)

        for radio in self.ui.repeatButtonContainer.findChildren(QRadioButton):
            radio.clicked.connect(self.repeat_button_handler)

        self.durationSlider.valueChanged.connect(self.duration_slider_value_change)
        self.inhaleSelectButton.clicked.connect(self.key_select_handler)
        self.exhaleSelectButton.clicked.connect(self.key_select_handler)
        self.confirmButton.clicked.connect(self.confirm_button_handler)

        self.key_select_modal.accepted.connect(self.handle_modal_finish)
        self.key_select_modal.setWindowModality(Qt.ApplicationModal)
        
        self.ui.optionsContainer.setEnabled(False)

        self.end_modal.finished.connect(self.finish_modal)
        # self.serialHandleClass.mesReceivedSignal.connect(self.message_received_handler)

    #defines selected_finger getter
    @property
    def selected_action(self):
        return self._selected_action

    #defines selected_finger setter and gives it runs value_reset_watcher
    @selected_action.setter
    def selected_action(self, action):
        self._selected_action = action
        self.value_reset_watcher()
        self.button_slider_state_handler(action)

    def selected_action_none_assign_watcher(self):
        if self.exhaleSlider.slider.value() == 0 and self.inhaleSlider.slider.value() == 0:
            logger.debug(f"selected_action_none_assign_watcher true")
            self.selected_action = None

    def button_slider_state_handler(self, action):
        if action == 1:
            self.inhaleSlider.slider.setValue(0)
            self.inhaleSelectButton.setEnabled(False)
            self.exhaleSelectButton.setEnabled(True)
            self.inhaleSelectButton.setText(self.string_list_components[0])
            self.param_select["key"] = None
        elif action == 2:
            self.exhaleSlider.slider.setValue(0)
            self.exhaleSelectButton.setEnabled(False)
            self.inhaleSelectButton.setEnabled(True)
            self.exhaleSelectButton.setText(self.string_list_components[0])
            self.param_select["key"] = None

    def set_slider_max_value(self,arry):
        for i,slider in enumerate(self.slider_array):
            slider.slider.setMaximum(arry[i])
            slider.maxLabel.setText(str(arry[i]/10) + 'kPa')
    
    def finish_modal(self):
        self.btSerialHandle.mesReceivedSignal.disconnect(self.message_received_handler)
        self.exhaleSlider.slider.setValue(0)
        self.inhaleSlider.slider.setValue(0)
    
    def duration_slider_value_change(self):
        print(f"slider: {self.sender().objectName()} - value: {self.sender().value()}")
        self.param_select.update({"duration":self.sender().value()})
        print(self.param_select)

    def confirm_button_handler(self):
        if self.selected_action == None:
            logger.debug("Selecione o valor de pressão de uma ação")
        elif self.param_select["key"] == None:
            warning = QMessageBox(self)
            warning.setWindowTitle(QCoreApplication.translate("ConfigJoystickDialogText",self.string_list_dialog[0]))
            warning.setText(QCoreApplication.translate("ConfigJoystickDialogText",self.string_list_dialog[1]))
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()
        else:
            self.setEnabled(False)
            messages, bindingDict = self.confirm_messages_generator()
            self.end_modal.sent_message_total = len(messages)  
            for message in messages:
                self.send_serial_message(message)
            self.jsonWriter.write_bindings(bindingDict)
            self.selected_action = None
            self.btSerialHandle.mesReceivedSignal.connect(self.message_received_handler)
            self.end_modal.exec()
            self.setEnabled(True)

    def key_select_handler(self):
        self.key_select_modal.exec()
    
    def repeat_button_handler(self):
        print(f"radio: {self.sender().objectName} - state: {self.sender().isChecked()}")
        if self.sender().objectName() == "repeatOffButton":
            self.param_select.update({"repeat_key":False})
        else:
            self.param_select.update({"repeat_key":True})
        print(self.param_select)
        
    def pressure_slider_value_change(self):
        print(f"slider: {self.sender().objectName()} - value: {self.sender().value()} - index: {self.sender().property("index")}")
        if self.sender().value() != 0:
            self.p_value = self.sender().value()
            self.selected_action = self.sender().property("index")
        else:
            self.selected_action_none_assign_watcher()
        self.sender().parent().parent().parent().currentLabel.setText(str(self.sender().value()/10) + 'kPa')

    def message_received_handler(self,response):
        self.end_modal.recieve_end_message(response)

    #resets info to be transmited via serial
    def value_reset_watcher(self):
        if self.ui.optionsContainer.isEnabled() == False:
            self.ui.optionsContainer.setEnabled(True)
        if self._selected_action == None:
            self.reset_variables()
            self.reset_screen()
            print(f"after reset:{self.param_select}")
            return True
        return False
    
    def reset_variables(self):
        self.param_select = param_select_base_val.copy()
        self.p_value = 0

    def reset_screen(self):
        self.repeatOffButton.setChecked(True)
        self.repeatOnButton.setChecked(False)
        print(f"reset_screen: {self.string_list_components[0]}")
        self.inhaleSelectButton.setText(self.string_list_components[0])
        self.exhaleSelectButton.setText(self.string_list_components[0])
        self.durationSlider.setValue(param_select_base_val["duration"])
        self.ui.optionsContainer.setEnabled(False)

    def send_serial_message(self,message):
        if self.btSerialHandle.bt_socket != None:
            self.btSerialHandle.open_port()
            # self.serialHandleClass.open_port()
            self.btSerialHandle.send_message(message)
            # self.serialHandleClass.send_message(message)
        
    def confirm_messages_generator(self):
        messages = []
        valueStr = None
        if(self.p_value < 10):#value always needs to be sent in a 3 digit format 
            valueStr = f"00{self.p_value}"
        elif(self.p_value < 100):
            valueStr = f"0{self.p_value}"
        #when sending the serial message, finger indexes start at 1
        messages.append("*M{}{}".format(self.selected_action,valueStr))#!p_values has to come first as to determine the function
        pairs = [(k, v) for (k, v) in self.param_select.items()]
        for i, (k,v) in enumerate(pairs):
            if v != None:
                match i:
                    case 0:
                        messages.append(f"*R{int(v)}")
                    case 1:
                        if self.selected_action == 1:
                            messages.append(f"*B{v}")
                        elif self.selected_action == 2:
                            messages.append(f"*U{v}")
                    case 2:
                        messages.append(f"*T{v}")
        bindingDict = {
                "repeat": self.param_select["repeat_key"],
                "duration": self.param_select["duration"],
                "key": self.param_select["key"],
                "pressure": self.p_value,
                "action": self.selected_action
        }
        return  messages, bindingDict
    
    def handle_modal_finish(self):#!beter logic maybe?
        key = self.key_select_modal.selected_key
        key_text = self.arrow_text_conversion(key)
        self.param_select.update({"key":key})
        if self.selected_action == 1:
            self.exhaleSelectButton.setText(key_text.upper())
        elif self.selected_action == 2:
            self.inhaleSelectButton.setText(key_text.upper())
        self.key_select_modal.selected_key = None

    def arrow_text_conversion(self,key):#chages literal word for directional arrows to icons
        key_text = key
        if key == "UP":
            key_text = str("↑")
        elif key == "DOWN":
            key_text = str("↓")
        elif key == "LEFT":
            key_text = str("←")
        elif key == "RIGHT":
            key_text = str("→")
        return key_text

    def assing_card_values(self,config):
        self.selected_action = False
        duration = int(config["duration"])
        repeat = True if config["repeat"] == "True" else False
        key = config["key"]
        pressure = int(config["pressure"])
        action = int(config["action"])-1
                
        self.slider_array[action].slider.setValue(pressure)
                
        self.durationSlider.setValue(duration)

        logger.debug(f"assing_card_values repeat:{repeat}")
        
        if repeat == True:
            self.repeatOnButton.setChecked(True)
            self.repeatOffButton.setChecked(False)
            self.param_select["repeat_key"] = True
        else:
            self.repeatOffButton.setChecked(True)
            self.repeatOnButton.setChecked(False)
            self.param_select["repeat_key"] = False
            
        self.key_select_modal.selected_key = key
        self.handle_modal_finish()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.string_list_components = [
                QCoreApplication.translate("ConfigJoystickComponents", "Clique para selecionar")
            ] 
            self.ui.retranslateUi(self)
            if self.param_select["key"] != None:
                key_text = self.arrow_text_conversion(self.param_select["key"])
                if self.selected_action == 2:
                    self.inhaleSelectButton.setText(key_text.upper())
                elif self.selected_action == 1:
                    self.exhaleSelectButton.setText(key_text.upper())
        return super().changeEvent(event)
        