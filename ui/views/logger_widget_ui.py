# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logger_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_loggerForm(object):
    def setupUi(self, loggerForm):
        if not loggerForm.objectName():
            loggerForm.setObjectName(u"loggerForm")
        loggerForm.resize(648, 445)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(loggerForm.sizePolicy().hasHeightForWidth())
        loggerForm.setSizePolicy(sizePolicy)
        loggerForm.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(loggerForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.windowContainer = QWidget(loggerForm)
        self.windowContainer.setObjectName(u"windowContainer")
        self.gridLayout_2 = QGridLayout(self.windowContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fullPairButton = QPushButton(self.windowContainer)
        self.fullPairButton.setObjectName(u"fullPairButton")

        self.verticalLayout.addWidget(self.fullPairButton)

        self.onOffButton = QPushButton(self.windowContainer)
        self.onOffButton.setObjectName(u"onOffButton")

        self.verticalLayout.addWidget(self.onOffButton)

        self.pairButton = QPushButton(self.windowContainer)
        self.pairButton.setObjectName(u"pairButton")

        self.verticalLayout.addWidget(self.pairButton)

        self.unpairButton = QPushButton(self.windowContainer)
        self.unpairButton.setObjectName(u"unpairButton")

        self.verticalLayout.addWidget(self.unpairButton)

        self.pairHidButton = QPushButton(self.windowContainer)
        self.pairHidButton.setObjectName(u"pairHidButton")

        self.verticalLayout.addWidget(self.pairHidButton)

        self.unpairHidButton = QPushButton(self.windowContainer)
        self.unpairHidButton.setObjectName(u"unpairHidButton")

        self.verticalLayout.addWidget(self.unpairHidButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.espItemContainer = QWidget(self.windowContainer)
        self.espItemContainer.setObjectName(u"espItemContainer")

        self.gridLayout_2.addWidget(self.espItemContainer, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.windowContainer, 0, 2, 1, 1)


        self.retranslateUi(loggerForm)

        QMetaObject.connectSlotsByName(loggerForm)
    # setupUi

    def retranslateUi(self, loggerForm):
        loggerForm.setWindowTitle(QCoreApplication.translate("loggerForm", u"Form", None))
        self.fullPairButton.setText(QCoreApplication.translate("loggerForm", u"Emparelhamento completo", None))
        self.onOffButton.setText(QCoreApplication.translate("loggerForm", u"Ligar/Desligar Bluetooth", None))
        self.pairButton.setText(QCoreApplication.translate("loggerForm", u"Emparelhar servi\u00e7o SPP", None))
        self.unpairButton.setText(QCoreApplication.translate("loggerForm", u"Desemparelhar servi\u00e7o SPP", None))
        self.pairHidButton.setText(QCoreApplication.translate("loggerForm", u"Emparelhar dispositivo HID", None))
        self.unpairHidButton.setText(QCoreApplication.translate("loggerForm", u"Desemparelhar dispositivo HID", None))
    # retranslateUi

