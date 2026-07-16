from ui.model.components.calibration_result_model import CalibrationResultModel

from shared_ui_modules.ui.model.stacked_widget_screens.calibration_shared_model import SharedCalibrationModel

from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel
from modules.bluetooth_serial_communication import BtSerialComm

from PySide6.QtCore import QCoreApplication, QEvent

class CalibrationWidgetModel(SharedCalibrationModel):

    def __init__(self,logModel: SharedLogModel | None, btSerialhandle: BtSerialComm | None):
        super().__init__( logModel, btSerialhandle)
        
        self.s_list = [
            "Sopre com toda força",
            "Inale com toda força"
        ]
        
        #modules setup
        self.logModel = logModel
        self.btSerialhandle = btSerialhandle

        self.setup_model()
        
    def get_step_1_presusre(self):
        return [0]

    def get_image_data(self):
        return [["_internal/resources/icons/exhale.png",250,250],["_internal/resources/icons/inhale.png",250,250]]

    def get_serial_messages(self):
        return ["*S1","*S2"]
    
    def get_str_array(self):
        return [
            QCoreApplication.translate(
                "InstructionText",
                "Sopre com toda força"
            ),
            QCoreApplication.translate(
                "InstructionText",
                "Inale com toda força"
            )
        ]

    def get_result_model(self):
        return CalibrationResultModel()
        
