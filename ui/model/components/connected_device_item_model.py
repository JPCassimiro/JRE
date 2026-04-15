from ui.views.connected_device_item_ui import Ui_selectedDeviceForm

from PySide6.QtWidgets import QWidget

class ConnectedDeviceModel(QWidget):
    
    def __init__(self,deviceInfoDict):
        
        super().__init__()

        #setup ui
        self.ui = Ui_selectedDeviceForm()
        self.ui.setupUi(self)

        #get ui elements
        self.macLabel = self.ui.macLabel
        self.comPortLabel = self.ui.comPortLabel
        self.hidCheckLabel = self.ui.hidCheckLabel
        self.sppCheckLabel = self.ui.sppCheckLabel
        self.deviceIconLabel = self.ui.deviceIconLabel
        self.deviceNameLabel = self.ui.deviceNameLabel
        
        self.device_info_dict = deviceInfoDict
        
        self.service_state = None
        self.device_state = None
        
        self.hidCheckLabel.hide()
        self.sppCheckLabel.hide()
        # self.deviceIconLabel.hide()

        self.update_fields(deviceInfoDict)
        print(f"ConnectedDeviceModel self.deviceIconLabel:{self.deviceIconLabel.pixmap()}")


    def update_fields(self,deviceInfoDict):
        self.macLabel.setText(deviceInfoDict["mac"])
        self.comPortLabel.setText(deviceInfoDict["port"])
        self.deviceNameLabel.setText(deviceInfoDict["name"])
        self.service_state = 1
        self.device_state = 1


        


    