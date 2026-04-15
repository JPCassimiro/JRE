# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'custom_slider_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

from ui.modifed_widgets.slider import Slider

class Ui_customSliderForm(object):
    def setupUi(self, customSliderForm):
        if not customSliderForm.objectName():
            customSliderForm.setObjectName(u"customSliderForm")
        customSliderForm.resize(100, 196)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(customSliderForm.sizePolicy().hasHeightForWidth())
        customSliderForm.setSizePolicy(sizePolicy)
        customSliderForm.setMinimumSize(QSize(100, 196))
        self.gridLayout = QGridLayout(customSliderForm)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.customSliderContainer = QWidget(customSliderForm)
        self.customSliderContainer.setObjectName(u"customSliderContainer")
        self.gridLayout_2 = QGridLayout(self.customSliderContainer)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.slider = QWidget(self.customSliderContainer)
        self.slider.setObjectName(u"slider")
        self.verticalLayout = QVBoxLayout(self.slider)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.maxLabel = QLabel(self.slider)
        self.maxLabel.setObjectName(u"maxLabel")

        self.verticalLayout.addWidget(self.maxLabel, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.verticalSlider = Slider(self.slider)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setMaximum(400)
        self.verticalSlider.setTracking(False)
        self.verticalSlider.setOrientation(Qt.Orientation.Vertical)

        self.verticalLayout.addWidget(self.verticalSlider, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.currentLabel = QLabel(self.slider)
        self.currentLabel.setObjectName(u"currentLabel")

        self.verticalLayout.addWidget(self.currentLabel, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.gridLayout_2.addWidget(self.slider, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.customSliderContainer, 0, 0, 1, 1)


        self.retranslateUi(customSliderForm)

        QMetaObject.connectSlotsByName(customSliderForm)
    # setupUi

    def retranslateUi(self, customSliderForm):
        customSliderForm.setWindowTitle(QCoreApplication.translate("customSliderForm", u"Form", None))
        self.maxLabel.setText(QCoreApplication.translate("customSliderForm", u"TextLabel", None))
        self.currentLabel.setText(QCoreApplication.translate("customSliderForm", u"TextLabel", None))
    # retranslateUi

