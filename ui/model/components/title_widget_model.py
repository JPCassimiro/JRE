from shared_ui_modules.ui.model.components.title_widget_model import SharedTitleWidgetModel

class TitleWidgetModel(SharedTitleWidgetModel):
    def __init__(self):
        super().__init__()

        self.initiate_module()

    def get_title_string(self):
        return "Joystick for Respiratory Exercicses"