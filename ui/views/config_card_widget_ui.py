# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_card_widget.ui'
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

class Ui_configCardWidgetForm(object):
    def setupUi(self, configCardWidgetForm):
        if not configCardWidgetForm.objectName():
            configCardWidgetForm.setObjectName(u"configCardWidgetForm")
        configCardWidgetForm.resize(184, 101)
        self.gridLayout_2 = QGridLayout(configCardWidgetForm)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        self.configCardContainer = QWidget(configCardWidgetForm)
        self.configCardContainer.setObjectName(u"configCardContainer")
        self.gridLayout = QGridLayout(self.configCardContainer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.otherInfoLabelContainer = QWidget(self.configCardContainer)
        self.otherInfoLabelContainer.setObjectName(u"otherInfoLabelContainer")
        self.horizontalLayout = QHBoxLayout(self.otherInfoLabelContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.durationIconLabel = QLabel(self.otherInfoLabelContainer)
        self.durationIconLabel.setObjectName(u"durationIconLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.durationIconLabel.sizePolicy().hasHeightForWidth())
        self.durationIconLabel.setSizePolicy(sizePolicy)
        self.durationIconLabel.setMinimumSize(QSize(16, 16))
        self.durationIconLabel.setMaximumSize(QSize(16, 16))
        self.durationIconLabel.setText(u"")
        self.durationIconLabel.setPixmap(QPixmap(u"_internal/resources/icons/timer.png"))
        self.durationIconLabel.setScaledContents(True)

        self.horizontalLayout.addWidget(self.durationIconLabel)

        self.durationLabel = QLabel(self.otherInfoLabelContainer)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setText(u"TextLabel")
        self.durationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.durationLabel)

        self.repeatIconLabel = QLabel(self.otherInfoLabelContainer)
        self.repeatIconLabel.setObjectName(u"repeatIconLabel")
        self.repeatIconLabel.setMinimumSize(QSize(16, 16))
        self.repeatIconLabel.setMaximumSize(QSize(16, 16))
        self.repeatIconLabel.setText(u"TextLabel")
        self.repeatIconLabel.setScaledContents(True)

        self.horizontalLayout.addWidget(self.repeatIconLabel)

        self.keyLabel = QLabel(self.otherInfoLabelContainer)
        self.keyLabel.setObjectName(u"keyLabel")
        self.keyLabel.setText(u"TextLabel")

        self.horizontalLayout.addWidget(self.keyLabel)


        self.gridLayout.addWidget(self.otherInfoLabelContainer, 1, 2, 1, 1)

        self.pressureLabelContainer = QWidget(self.configCardContainer)
        self.pressureLabelContainer.setObjectName(u"pressureLabelContainer")
        self.gridLayout_3 = QGridLayout(self.pressureLabelContainer)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.actionLabel = QLabel(self.pressureLabelContainer)
        self.actionLabel.setObjectName(u"actionLabel")

        self.gridLayout_3.addWidget(self.actionLabel, 0, 0, 1, 1)

        self.pressureLabel = QLabel(self.pressureLabelContainer)
        self.pressureLabel.setObjectName(u"pressureLabel")

        self.gridLayout_3.addWidget(self.pressureLabel, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.pressureLabelContainer, 0, 2, 1, 1)


        self.gridLayout_2.addWidget(self.configCardContainer, 0, 0, 1, 1)


        self.retranslateUi(configCardWidgetForm)

        QMetaObject.connectSlotsByName(configCardWidgetForm)
    # setupUi

    def retranslateUi(self, configCardWidgetForm):
        configCardWidgetForm.setWindowTitle(QCoreApplication.translate("configCardWidgetForm", u"Form", None))
#if QT_CONFIG(tooltip)
        configCardWidgetForm.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.durationIconLabel.setToolTip(QCoreApplication.translate("configCardWidgetForm", u"Tempo de press\u00e3o necessario para ativa\u00e7\u00e3o", u"configCardhelper"))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.repeatIconLabel.setToolTip(QCoreApplication.translate("configCardWidgetForm", u"Repeti\u00e7\u00e3o ativada/desativada", u"configCardhelper"))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.keyLabel.setToolTip(QCoreApplication.translate("configCardWidgetForm", u"Teclas a ser emulada", u"configCardhelper"))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pressureLabelContainer.setToolTip(QCoreApplication.translate("configCardWidgetForm", u"Press\u00f5es associadas a cada dedo", u"configCardhelper"))
#endif // QT_CONFIG(tooltip)
        self.actionLabel.setText(QCoreApplication.translate("configCardWidgetForm", u"Exerc\u00edcio:", None))
        self.pressureLabel.setText(QCoreApplication.translate("configCardWidgetForm", u"Press\u00e3o (kPa):", None))
    # retranslateUi

