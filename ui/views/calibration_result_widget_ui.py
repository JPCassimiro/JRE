# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calibration_result_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_calibrationResultWidget(object):
    def setupUi(self, calibrationResultWidget):
        if not calibrationResultWidget.objectName():
            calibrationResultWidget.setObjectName(u"calibrationResultWidget")
        calibrationResultWidget.resize(590, 310)
        self.gridLayout = QGridLayout(calibrationResultWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.resultContainer = QWidget(calibrationResultWidget)
        self.resultContainer.setObjectName(u"resultContainer")
        self.horizontalLayout = QHBoxLayout(self.resultContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.exhaleContainer = QWidget(self.resultContainer)
        self.exhaleContainer.setObjectName(u"exhaleContainer")
        self.horizontalLayout_2 = QHBoxLayout(self.exhaleContainer)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 2, -1, 2)
        self.exhaleIconLabel = QLabel(self.exhaleContainer)
        self.exhaleIconLabel.setObjectName(u"exhaleIconLabel")
        self.exhaleIconLabel.setMinimumSize(QSize(256, 256))
        self.exhaleIconLabel.setMaximumSize(QSize(256, 256))
        self.exhaleIconLabel.setPixmap(QPixmap(u"_internal/resources/icons/exhale.png"))
        self.exhaleIconLabel.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.exhaleIconLabel)


        self.horizontalLayout.addWidget(self.exhaleContainer)

        self.inhaleContainer = QWidget(self.resultContainer)
        self.inhaleContainer.setObjectName(u"inhaleContainer")
        self.horizontalLayout_3 = QHBoxLayout(self.inhaleContainer)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, -1, 2)
        self.inhaleIconLabel = QLabel(self.inhaleContainer)
        self.inhaleIconLabel.setObjectName(u"inhaleIconLabel")
        self.inhaleIconLabel.setMinimumSize(QSize(256, 256))
        self.inhaleIconLabel.setMaximumSize(QSize(256, 256))
        self.inhaleIconLabel.setPixmap(QPixmap(u"_internal/resources/icons/inhale.png"))
        self.inhaleIconLabel.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.inhaleIconLabel)


        self.horizontalLayout.addWidget(self.inhaleContainer)


        self.gridLayout.addWidget(self.resultContainer, 0, 0, 1, 1)


        self.retranslateUi(calibrationResultWidget)

        QMetaObject.connectSlotsByName(calibrationResultWidget)
    # setupUi

    def retranslateUi(self, calibrationResultWidget):
        calibrationResultWidget.setWindowTitle(QCoreApplication.translate("calibrationResultWidget", u"Form", None))
        self.exhaleIconLabel.setText("")
        self.inhaleIconLabel.setText("")
    # retranslateUi

