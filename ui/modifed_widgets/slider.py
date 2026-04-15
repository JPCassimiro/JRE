from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

#when recompiled, this class needs to be imported to config_widget_ui
#allows the slider to be clicked, not dragged
class Slider(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 400)
    
    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            length = self.height()
            click_pos = event.position().y()
            ratio = (length - click_pos) / length
            value = ratio * self.maximum()
            self.setValue(int(value))
            event.accept()
        else:
            return super().mousePressEvent(event)