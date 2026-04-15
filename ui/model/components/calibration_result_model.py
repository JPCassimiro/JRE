from ui.views.calibration_result_widget_ui import Ui_calibrationResultWidget
from PySide6.QtWidgets import QWidget
from ui.model.custom_widgets.custom_slider_model import CustomSliderModel
from PySide6.QtCore import QRect
from modules.log_class import logger

class CalibrationResultModel(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_calibrationResultWidget()
        self.ui.setupUi(self)

        #hand sliders
        self.exhaleSlider = CustomSliderModel()
        self.inhaleSlider = CustomSliderModel()
        
        self.exhaleContainer = self.ui.exhaleContainer
        self.inhaleContainer = self.ui.inhaleContainer
        
        self.slider_array = [
            self.exhaleSlider,
            self.inhaleSlider,
        ]
        
        self.exhaleSlider.slider.setProperty("index",0)
        self.inhaleSlider.slider.setProperty("index",1)

        self.exhaleContainer.layout().addWidget(self.exhaleSlider)
        self.inhaleContainer.layout().addWidget(self.inhaleSlider)

        for slider in self.slider_array:
            slider.slider.setEnabled(False)

    def set_pressure_values(self, value_array=None):
        try:
            if value_array:
                logger.debug(f"Valores de pressão recebidos: ")
                for i,slider in enumerate(self.slider_array):
                    slider.slider.setValue(value_array[i])
                    slider.currentLabel.setText(str(value_array[i]/10) + 'kPa')
                    slider.maxLabel.setText(str(slider.slider.maximum()/10) + 'kPa')
                    logger.debug(f"{value_array[i]/10} KG")
            else:
                logger.error(f"Valores de pressão não foram recebidos na tela de resultados - value_array: {value_array}")
        except Exception as e:
            logger.error(f"Erro ao tentar apresentar o resultado da calibração: {e}")
