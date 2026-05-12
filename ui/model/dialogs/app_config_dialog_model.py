from shared_ui_modules.ui.model.dialogs.app_config_dialog_model import SharedAppConfigModel

class AppConfigDialogModel(SharedAppConfigModel):
    def __init__(self):
        super().__init__()

        self.initialize_module()
        
    def get_api_endpoint(self):
        return "https://api.github.com/repos/JPCassimiro/JRE/releases/latest"

    #!change this on every new release
    def get_version_name(self):
        return "Stable V1.0.1"