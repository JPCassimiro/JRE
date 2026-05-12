from shared_ui_modules.modules.bluetooth_serial_communication import SharedBtSerialComm

class BtSerialComm(SharedBtSerialComm):
    def __init__(self):
        super().__init__()

        self.initialize_module()

    def get_fake_data(self):
        return ["*I020100","*I100200","*I000120","*I020020"]

    def get_use_data_get_regex(self):
        return r"\*I\d{6}"