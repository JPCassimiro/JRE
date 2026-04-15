from ui.views.custom_slider_widget_ui import Ui_customSliderForm
from PySide6.QtWidgets import QWidget, QStyle, QStyleOptionSlider

class CustomSliderModel(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_customSliderForm()
        self.ui.setupUi(self)
        
        self.slider = self.ui.verticalSlider
        self.maxLabel = self.ui.maxLabel
        self.currentLabel = self.ui.currentLabel
        
        self.setFixedWidth(60)#min
        
        self.maxLabel.setText(str(self.slider.maximum()/10) + "kPa")
        self.currentLabel.setText(str(self.slider.value()/10) + "kPa")

        self.slider.valueChanged.connect(self.adjust_roundness)
        
        
    def adjust_roundness(self):
        # opt = QStyleOptionSlider()
        # opt.initFrom(self.slider)
        # opt.orientation = self.slider.orientation()
        # opt.minimum = self.slider.minimum()
        # opt.maximum = self.slider.maximum()
        # opt.tickPosition = self.slider.tickPosition()
        # opt.sliderPosition = self.slider.sliderPosition()
        # opt.sliderValue = self.slider.value()
        # rect = self.slider.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_ScrollBarSlider, self.slider)
        # print(f"CustomSliderModel adjust_roundness - size:{rect.size()}")

        if self.slider.value() <= (self.slider.maximum())*0.15:
            self.slider.setStyleSheet("""
                QWidget#slider>QSlider::add-page{
                border-radius: 5px;}""")
        if self.slider.value() <= (self.slider.maximum())*0.125:
            self.slider.setStyleSheet("""
                QWidget#slider>QSlider::add-page{
                border-radius: 4px;}""")
        if self.slider.value() <= (self.slider.maximum())*0.1:
            self.slider.setStyleSheet("""
                QWidget#slider>QSlider::add-page{
                border-radius: 2px;}""")
        if self.slider.value() <= (self.slider.maximum())*0.075:
            self.slider.setStyleSheet("""
                QWidget#slider>QSlider::add-page{
                border-radius: 1px;}""")
        if self.slider.value() >= (self.slider.maximum())*0.155:
            self.slider.setStyleSheet("""
                QWidget#slider>QSlider::add-page{
                border-radius: 6px;}""")
        