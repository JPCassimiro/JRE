from ui.views.custom_slider_widget_ui import Ui_customSliderForm

from shared_ui_modules.modules.log_class import logger

from PySide6.QtWidgets import QWidget, QStyle, QStyleOptionSlider

class CustomSliderModel(QWidget):
    def __init__(self,unit):
        super().__init__()

        self.ui = Ui_customSliderForm()
        self.ui.setupUi(self)
        
        self.unit = unit
        self.slider = self.ui.verticalSlider
        self.maxLabel = self.ui.maxLabel
        self.currentLabel = self.ui.currentLabel
        
        self.setFixedWidth(60)#min
        self.slider.setMaximum(400)
        
        self.maxLabel.setText(str(self.slider.maximum()/10) + self.unit)
        self.currentLabel.setText(str(self.slider.value()/10) + self.unit)

        # self.slider.valueChanged.connect(self.adjust_roundness)
        self.slider.valueChanged.connect(self.assing_current_label_value)
        self.slider.rangeChanged.connect(self.adjust_max_label)    
    
    def adjust_max_label(self):
        self.maxLabel.setText(str(self.slider.maximum()/10) + self.unit)
    
    def assing_current_label_value(self,val):    
        self.currentLabel.setText(str(val/10) + self.unit)
        
    # def adjust_roundness(self):
    #     try:
    #         # opt = QStyleOptionSlider()
    #         # opt.initFrom(self.slider)
    #         # opt.orientation = self.slider.orientation()
    #         # opt.minimum = self.slider.minimum()
    #         # opt.maximum = self.slider.maximum()
    #         # opt.tickPosition = self.slider.tickPosition()
    #         # opt.sliderPosition = self.slider.sliderPosition()
    #         # opt.sliderValue = self.slider.value()
    #         # rect = self.slider.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_ScrollBarSlider, self.slider)

    #         # if self.slider.value() <= (self.slider.maximum())*0.15:
    #         #     self.slider.setStyleSheet("""
    #         #         QWidget#slider>QSlider::add-page{
    #         #         border-radius: 5px;}""")
    #         # if self.slider.value() <= (self.slider.maximum())*0.125:
    #         #     self.slider.setStyleSheet("""
    #         #         QWidget#slider>QSlider::add-page{
    #         #         border-radius: 4px;}""")
    #         # if self.slider.value() <= (self.slider.maximum())*0.1:
    #         #     self.slider.setStyleSheet("""
    #         #         QWidget#slider>QSlider::add-page{
    #         #         border-radius: 2px;}""")
    #         # if self.slider.value() <= (self.slider.maximum())*0.075:
    #         #     self.slider.setStyleSheet("""
    #         #         QWidget#slider>QSlider::add-page{
    #         #         border-radius: 1px;}""")
    #         # if self.slider.value() >= (self.slider.maximum())*0.155:
    #         #     self.slider.setStyleSheet("""
    #         #         QWidget#slider>QSlider::add-page{
    #         #         border-radius: 6px;}""")
    #     except Exception as e:
    #         logger.error(f"CustomSliderModel adjust_roundness error: {e}")