from modules.json_writer import JsonWriterClass

from shared_ui_modules.ui.model.stacked_widget_screens.connection_manager_model import SharedConnectionManagerModel

#basic widget funcionalitty
    #list all available joysticks
    #allow joystick connection using button
    #conncetion 
        #disconnect currently connected joystikc
        #connect new joystick

class ConnectionManagerModel(SharedConnectionManagerModel):

    def __init__(self,  logModel, serialBtClass):

        super().__init__(  logModel, serialBtClass)
        
        self.setup_module()

    def get_json_writer(self):
        return JsonWriterClass()