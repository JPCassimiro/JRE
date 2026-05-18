from shared_ui_modules.ui.model.stacked_widget_screens.user_actions_widget_model import SharedUserActionsModel

class UserActionsModel(SharedUserActionsModel):
    
    def __init__(self, dbHandleClass,logModel):
        super().__init__(dbHandleClass,logModel)