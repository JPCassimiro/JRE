from ui.views.config_widget_ui import Ui_configForm

from shared_ui_modules.ui.model.dialogs.key_select_model import SharedKeySelectModel
from shared_ui_modules.ui.model.components.end_config_model import SharedEndConfigModel
from shared_ui_modules.ui.model.stacked_widget_screens.config_widget_model import SharedConfigWidgetModel

from ui.model.custom_widgets.custom_slider_model import CustomSliderModel

from shared_ui_modules.modules.log_class import logger
from modules.json_writer import JsonWriterClass
from modules.bluetooth_serial_communication import BtSerialComm
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel

from PySide6.QtWidgets import QWidget, QRadioButton, QMessageBox, QSpacerItem, QSizePolicy
from PySide6.QtCore import QRect, Qt, QCoreApplication, QEvent


param_select_base_val = {
    "key_1":None,
    "key_2":None,
    "repeat_key":False,
    "duration":0
}

class ConfigWidgetModel(SharedConfigWidgetModel):
    def __init__(self, btSerialHandle: BtSerialComm | None, LogModel: SharedLogModel | None):
        super().__init__(btSerialHandle, LogModel)

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

        self.key_select_modal = SharedKeySelectModel()
        self.end_modal = SharedEndConfigModel()
        self.logModel = LogModel
        self.btSerialHandle = btSerialHandle
        self.jsonWriter = JsonWriterClass()

        #variables setup
        self.param_select = param_select_base_val.copy()
        self._p_value = [0,0]
        self.current_user = None
        self.selected_button = None
        
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
        self.resetExhalePressureValueButton = self.ui.resetExhalePressureValue
        self.resetInhalePressureValueButton = self.ui.resetInhalePressureValue

        self.inhaleSelectButton.setEnabled(False)
        self.exhaleSelectButton.setEnabled(False)

        self.exhaleSlider.slider.setProperty("index",1)
        self.inhaleSlider.slider.setProperty("index",2)
        self.exhaleSelectButton.setProperty("index",1)
        self.inhaleSelectButton.setProperty("index",2)
        self.resetExhalePressureValueButton.setProperty("index",1)
        self.resetInhalePressureValueButton.setProperty("index",2)

        #add sliders to screen
        self.ui.exhaleSliderContainer.layout().insertWidget(0,self.exhaleSlider)
        self.ui.exhaleSliderContainer.layout().insertSpacerItem(0, self.exhaleSpacer)
        self.ui.exhaleSliderContainer.layout().addSpacerItem(self.exhaleSpacer)
        
        self.ui.inhaleSliderContainer.layout().insertWidget(0,self.inhaleSlider)
        self.ui.inhaleSliderContainer.layout().insertSpacerItem(0, self.inhaleSpacer)
        self.ui.inhaleSliderContainer.layout().addSpacerItem(self.inhaleSpacer)
        
        #connections
        for slider in self.slider_array:
            slider.setEnabled(True)
            slider.slider.valueChanged.connect(self.pressure_slider_value_change)
            slider.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for radio in self.ui.repeatButtonContainer.findChildren(QRadioButton):
            radio.clicked.connect(self.repeat_button_handler)

        self.durationSlider.valueChanged.connect(self.duration_slider_value_change)
        self.inhaleSelectButton.clicked.connect(self.key_select_handler)
        self.exhaleSelectButton.clicked.connect(self.key_select_handler)
        self.confirmButton.clicked.connect(self.confirm_button_handler)
        self.resetInhalePressureValueButton.clicked.connect(self.reset_slider_value_button_handler)
        self.resetExhalePressureValueButton.clicked.connect(self.reset_slider_value_button_handler)

        self.key_select_modal.accepted.connect(self.handle_modal_finish)
        self.key_select_modal.setWindowModality(Qt.ApplicationModal)
        
        self.ui.optionsContainer.setEnabled(False)

        self.end_modal.finished.connect(self.finish_modal)
        # self.serialHandleClass.mesReceivedSignal.connect(self.message_received_handler)

    #defines selected_finger getter
    @property
    def p_value(self):
        return self._p_value

    #defines selected_finger setter and gives it runs value_reset_watcher
    @p_value.setter
    def p_value(self, index_value):
        index, value = index_value
        self._p_value[index] = value
        self.value_reset_watcher()
        self.button_slider_state_handler()

    def reset_slider_value_button_handler(self):
        index = self.sender().property("index")
        match index:
            case 1:
                self.exhaleSlider.slider.setValue(0)
            case 2:
                self.inhaleSlider.slider.setValue(0)

    def button_slider_state_handler(self):
        try:    
            #if p_value[0] or [1] equals 0, reset button text, reset param_select key, reset button state
            if self.p_value[0] == 0:
                if self.exhaleSelectButton.isEnabled() == True:
                    self.exhaleSelectButton.setEnabled(False)
                self.exhaleSelectButton.setText(self.string_list_components[0])
                self.param_select.update({"key_1":None})
            else:
                if self.exhaleSelectButton.isEnabled() == False:
                    self.exhaleSelectButton.setEnabled(True)
            if self.p_value[1] == 0:
                self.inhaleSelectButton.setEnabled(False)
                self.inhaleSelectButton.setText(self.string_list_components[0])
                self.param_select.update({"key_2":None})
            else:
                if self.inhaleSelectButton.isEnabled() == False:
                    self.inhaleSelectButton.setEnabled(True)
        except Exception as e:
            logger.error(f"ConfigWidgetModel button_slider_state_handler error: {e}")

    def set_slider_max_value(self,arry):
        try:
            for i,slider in enumerate(self.slider_array):
                slider.slider.setMaximum(arry[i])
                slider.maxLabel.setText(str(arry[i]/10) + 'kPa')
        except Exception as e:
            logger.error(f"ConfigWidgetModel set_slider_max_value error: {e}")
    
    def finish_modal(self):
        try:
            self.btSerialHandle.mesReceivedSignal.disconnect(self.message_received_handler)
            self.exhaleSlider.slider.setValue(0)
            self.inhaleSlider.slider.setValue(0)
        except Exception as e:
            logger.error(f"ConfigWidgetModel finish_modal error: {e}")

    def duration_slider_value_change(self):
        try:
            self.param_select.update({"duration":self.sender().value()})
        except Exception as e:
            logger.error(f"ConfigWidgetModel duration_slider_value_change error: {e}")

    def confirm_check(self):
        try:
            logger.debug(f"ConfigWidgetModel confirm_check - p_value: {self.p_value} - self.param_select: {self.param_select}")
            if self.param_select["key_1"] == None and self.param_select["key_2"] == None:     
                logger.debug(f"confirm_check true no key") 
                return True
            elif self.p_value[0] > 0 and self.param_select["key_1"] == None:
                logger.debug(f"confirm_check true no key_1") 
                return True
            elif self.p_value[1] > 0 and self.param_select["key_2"] == None:
                logger.debug(f"confirm_check true no key_2") 
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"ConfigWidgetModel confirm_check error: {e}")

    def start_config_process(self):
        try:
            check = self.confirm_check()
            if self.btSerialHandle.socket_none_check():
                raise Exception("null socket")
            elif check:
                warning = QMessageBox(self)
                warning.setWindowTitle(QCoreApplication.translate("ConfigJoystickDialogText",self.string_list_dialog[0]))
                warning.setText(QCoreApplication.translate("ConfigJoystickDialogText",self.string_list_dialog[1]))
                warning.setWindowModality(Qt.ApplicationModal)
                warning.show()
            else:
                self.setEnabled(False)
                messages, bindingArray = self.confirm_messages_generator()
                self.end_modal.sent_message_total = len(messages)  
                for message in messages:
                    self.send_serial_message(message)
                self.jsonWriter.write_bindings(bindingArray)
                self.btSerialHandle.mesReceivedSignal.connect(self.message_received_handler)
                self.end_modal.exec()
                self.setEnabled(True)
        except Exception as e:
            logger.error(f"ConfigWidgetModel start_config_process error: {e}")
            self._p_value = [0,0]
            self.p_value = (0,0)
            self.reset_variables()
            self.reset_screen()
            raise

    def key_select_handler(self):
        try:
            self.selected_button = self.sender().property("index")
            self.key_select_modal.exec()
        except Exception as e:
            logger.error(f"ConfigWidgetModel key_select_handler error: {e}")
    
    def pressure_slider_value_change(self):
        try:
            self.p_value = (self.sender().property("index")-1, self.sender().value())
            self.latest_change = self.sender().property("index")
            self.sender().parent().parent().parent().currentLabel.setText(str(self.sender().value()/10) + 'kPa')
        except Exception as e:
            logger.error(f"ConfigWidgetModel pressure_slider_value_change error: {e}")

    #resets info to be transmited via serial
    def value_reset_watcher(self):
        try:
            if self.ui.optionsContainer.isEnabled() == False:
                self.ui.optionsContainer.setEnabled(True)
            if self.p_value[0] == 0 and self.p_value[1] == 0:
                self.reset_variables()
                self.reset_screen()
                logger.debug(f"after reset: {self.param_select}")
                return True
            return False
        except Exception as e:
            logger.error(f"ConfigWidgetModel value_reset_watcher error: {e}")
    
    def reset_variables(self):
        try:
            self.param_select = param_select_base_val.copy()
            self.selected_button = None
        except Exception as e:
            logger.error(f"ConfigWidgetModel reset_variables error: {e}")

    def reset_screen(self):
        try:
            self.repeatOffButton.setChecked(True)
            self.repeatOnButton.setChecked(False)
            self.inhaleSelectButton.setText(self.string_list_components[0])
            self.exhaleSelectButton.setText(self.string_list_components[0])
            self.durationSlider.setValue(param_select_base_val["duration"])
            self.ui.optionsContainer.setEnabled(False)
            self.exhaleSlider.slider.setValue(0)
            self.inhaleSlider.slider.setValue(0)
        except Exception as e:
            logger.error(f"ConfigWidgetModel reset_screen error: {e}")
        
    def confirm_messages_generator(self):
        try:
            messages = []
            bindingArray = []
            
            for index, p in enumerate(self.p_value):
                if p != 0:
                    mes = self.message_normalization(p,index+1)                
                    messages.append(mes)#!p_values has to come first as to determine the function
                    key = self.param_select[f"key_{index+1}"]
                    duration = self.param_select["duration"]
                    repeat = self.param_select["repeat_key"]
                    
                    if key != None:
                        if index == 0:
                            messages.append(f"*B{key}")
                        elif index == 1:
                            messages.append(f"*U{key}")

                    if repeat != None:
                        messages.append(f"*R{int(repeat)}")

                    if duration != None:
                        messages.append(f"*T{duration}")

                    bindingArray.append({
                            "repeat": self.param_select["repeat_key"],
                            "duration": self.param_select["duration"],
                            "key": self.param_select[f"key_{index+1}"],
                            "pressure": self.p_value[index],
                            "action": index+1
                        })
                            
            return  messages, bindingArray
        except Exception as e:
            logger.error(f"ConfigWidgetModel confirm_messages_generator error: {e}")
            raise
    
    def handle_modal_finish(self):#!beter logic maybe?
        try:
            key = self.key_select_modal.selected_key
            key_text = self.arrow_text_conversion(key)
            logger.debug(f"handle_modal_finish self.selected_button: {self.selected_button}")
            if self.selected_button == 1:
                self.param_select.update({"key_1":key})
                self.exhaleSelectButton.setText(key_text.upper())
            elif self.selected_button == 2:
                self.param_select.update({"key_2":key})
                self.inhaleSelectButton.setText(key_text.upper())
            self.key_select_modal.selected_key = None
        except Exception as e:
            logger.error(f"ConfigWidgetModel handle_modal_finish error: {e}")

    def assing_card_values(self,config):
        try:
            if config is None:
                raise Exception(f"null config: {config}")
            duration = int(config["duration"])
            repeat = bool(config["repeat"])
            key = config["key"]
            pressure = int(config["pressure"])
            action = int(config["action"])-1
                    
            self.slider_array[action].slider.setValue(pressure)
                    
            self.durationSlider.setValue(duration)

            if repeat == True:
                self.repeatOnButton.setChecked(True)
                self.repeatOffButton.setChecked(False)
                self.param_select["repeat_key"] = True
            else:
                self.repeatOffButton.setChecked(True)
                self.repeatOnButton.setChecked(False)
                self.param_select["repeat_key"] = False
                
            self.selected_button = int(config["action"])
            self.key_select_modal.selected_key = key
            self.handle_modal_finish()
        except Exception as e:
            logger.error(f"ConfigWidgetModel assing_card_values error: {e}")
        
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.string_list_components = [
                QCoreApplication.translate("ConfigJoystickComponents", "Clique para selecionar")
            ] 
            self.ui.retranslateUi(self)
            keys = [self.param_select["key_1"], self.param_select["key_2"]]
            for i,k in enumerate(keys):
                if k != None:
                    key_text = self.arrow_text_conversion(k)
                    if i == 1:
                        self.inhaleSelectButton.setText(key_text.upper())
                    elif i == 0:
                        self.exhaleSelectButton.setText(key_text.upper())
        return super().changeEvent(event)