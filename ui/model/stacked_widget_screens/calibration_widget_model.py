from ui.views.calibration_widget_ui import Ui_calibrationForm
from ui.model.components.calibration_result_model import CalibrationResultModel
from modules.log_class import logger

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, Signal, QCoreApplication, QEvent

class CalibrationWidgetModel(QWidget):

    pValuesSignal = Signal(list)
    sideMenuDisableSignal = Signal(bool)
    
    def __init__(self,serialHandleClass,logModel,btSerialhandle):
        super().__init__()
        
        self.string_list_instruction = [
            QCoreApplication.translate("InstructionText","Sopre com toda força"),
            QCoreApplication.translate("InstructionText","Inale com toda força")
        ]
        
        #setup ui
        self.ui = Ui_calibrationForm()
        self.ui.setupUi(self)
        
        #modules setup
        self.serialHandleClass = serialHandleClass
        self.timer = QTimer()
        self.logModel = logModel
        self.btSerialhandle = btSerialhandle
        
        #custom ui element setup
        self.resultModel = CalibrationResultModel()
        self.ui.visualsContainer.layout().addWidget(self.resultModel)
        self.resultModel.hide()

        #variables
        self.exhale_pressure = [0]
        self.inhale_pressure = [0]
        self.timeout_counter = 0
        self.serial_messages = ["*S1","*S2"]
        self.calibration_step = 0

        #get ui elements
        self.startButton = self.ui.startButton
        self.instructionText = self.ui.instructionLabel
        self.cancelButton = self.ui.cancelButton
        self.restartButton = self.ui.restartButton
        self.imgLabel = self.ui.imgLabel
        
        self.cancelButton.setEnabled(False)

        self.image_data = [["_internal/resources/icons/exhale.png",250,250],["_internal/resources/icons/inhale.png",250,250]]
        # self.instructionText.setText(QCoreApplication.translate("InstructionText",self.string_list_instruction[0]))
        self.update_instruction_ui()

        #connections
        self.startButton.clicked.connect(self.start_button_handler)
        self.timer.timeout.connect(self.timeout_handler)
        self.restartButton.clicked.connect(self.restart_calibration)
        self.cancelButton.clicked.connect(self.cancel_button_handler)
        
    def set_instruction_image(self,img_path,width,height):
        try:
            img = QPixmap()
            if img.load(img_path):
                self.imgLabel.clear()
                self.imgLabel.setMinimumHeight(0)
                self.imgLabel.setMinimumWidth(0)
                self.imgLabel.setMaximumWidth(width)
                self.imgLabel.setMaximumHeight(height)
                self.imgLabel.updateGeometry()
                self.imgLabel.setPixmap(img)
                self.imgLabel.setScaledContents(True)

            else:
                logger.error(f"Erro ao cerregar imagem no caminho: {img_path}")
        except Exception as e:
            logger.error(f"Erro ao atribuir uma imagem de instrução: {e}")
        
    def cancel_button_handler(self):
        self.timer.stop()
        self.timeout_counter = 0
        self.ui_counter = 0        
        if self.calibration_step == 0:
            self.exhale_pressure = [0]
        else:
            self.inhale_pressure = [0]
        self.cancelButton.setEnabled(False)
        self.restartButton.setEnabled(True)
        self.startButton.setEnabled(True)
        self.sideMenuDisableSignal.emit(True)
        self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
        self.btSerialhandle.port_error.disconnect(self.port_error_handle)
        
    #starts the timer
    #500ms timer for sending the messages
    def start_button_handler(self):
        self.startButton.setEnabled(False)
        self.restartButton.setEnabled(False)
        # self.serialHandleClass.mesReceivedSignal.connect(self.recieve_serial_message)
        self.btSerialhandle.mesReceivedSignal.connect(self.recieve_serial_message)
        self.btSerialhandle.port_error.connect(self.port_error_handle)
        self.cancelButton.setEnabled(True)
        self.timer.start(500)
        self.sideMenuDisableSignal.emit(False)

    def port_error_handle(self):
        self.logModel.append_log(f"Dispositivo não conectado")
        self.cancel_button_handler()
        
    #messages are to be sent in *S1 to *S4 order
    def send_serial_message(self,message):
        # self.serialHandleClass.open_port()
        self.btSerialhandle.open_port()
        # self.serialHandleClass.send_message(message)
        self.btSerialhandle.send_message(message)
    
    #messages will be recieved in the same order as they are sent, per serial rules
    def recieve_serial_message(self,recieved):
        self.logModel.append_log(recieved)
        if self.calibration_step == 0:
            self.exhale_pressure.append(int(recieved[:3]))
        else:
            self.inhale_pressure.append(int(recieved[:3]))
        
    def restart_calibration(self):
        self.reset_variables()
        self.reset_screen()
        
    def reset_variables(self):
        self.exhale_pressure = [0]
        self.inhale_pressure = [0]
        self.timeout_counter = 0
        self.calibration_step = 0
        
    def reset_screen(self):
        # self.instructionText.setText(QCoreApplication.translate("InstructionText",self.string_list_instruction[1]))
        self.resultModel.hide()
        self.instructionText.show()
        self.imgLabel.show()
        self.update_instruction_ui()
        self.startButton.setEnabled(True)

        
    def present_results(self):
        self.imgLabel.hide()
        self.instructionText.hide()
        self.resultModel.show()
        self.startButton.setDisabled(True)
        max_val_array = self.get_max_pressure_values()
        #self.pValuesSignal.emit(max_val_array)
        self.resultModel.set_pressure_values([max_val_array[0],max_val_array[1],0,0,0])
        
    def get_max_pressure_values(self):
        max_val_array = []
        if self.exhale_pressure:
            max_val_array.append(max(self.exhale_pressure))
            max_val_array.append(max(self.inhale_pressure))
            return max_val_array

    #11 timeouts in total
    #so 5.5 seconds total duration
    #first timer does nothing
    #starting from the second timer, or first timeout
        #sends 4 mesages
    #on final timeout
        #reenable screen
    def timeout_handler(self):
        if self.calibration_step == 0:
            if self.timeout_counter < 10:
                self.send_serial_message(self.serial_messages[0])
                self.timeout_counter += 1
                return
            else:
                self.timeout_counter = 0
                self.startButton.setEnabled(True)
                self.restartButton.setEnabled(True)
                self.cancelButton.setEnabled(False)
                self.sideMenuDisableSignal.emit(True)
                # self.instructionText.setText(QCoreApplication.translate("InstructionText",self.string_list_instruction[1]))
                self.calibration_step = 1
                self.update_instruction_ui()
                self.timer.stop()
                self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
                self.btSerialhandle.port_error.disconnect(self.port_error_handle)
                # self.serialHandleClass.mesReceivedSignal.disconnect(self.recieve_serial_message)
                return
            
        elif self.calibration_step == 1:
            if self.timeout_counter < 10:
                self.send_serial_message(self.serial_messages[1])
                self.timeout_counter += 1
                return
            else:
                self.timeout_counter = 0
                self.calibration_step = 0
                self.timer.stop()
                self.btSerialhandle.mesReceivedSignal.disconnect(self.recieve_serial_message)
                self.btSerialhandle.port_error.disconnect(self.port_error_handle)
                # self.serialHandleClass.mesReceivedSignal.disconnect(self.recieve_serial_message)
                self.startButton.setEnabled(True)
                self.restartButton.setEnabled(True)
                self.cancelButton.setEnabled(False)
                self.sideMenuDisableSignal.emit(True)
                self.present_results()
                return

    def update_instruction_ui(self):
        self.string_list_instruction = [
            QCoreApplication.translate("InstructionText","Sopre com toda força"),
            QCoreApplication.translate("InstructionText","Inale com toda força")
        ]
        if self.calibration_step == 0:
            self.instructionText.setText(self.string_list_instruction[0])
            self.set_instruction_image(self.image_data[0][0],self.image_data[0][1],self.image_data[0][2])
        elif self.calibration_step == 1:
            self.instructionText.setText(self.string_list_instruction[1])
            self.set_instruction_image(self.image_data[1][0],self.image_data[1][1],self.image_data[1][2])


    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.update_instruction_ui()
        return super().changeEvent(event)
        