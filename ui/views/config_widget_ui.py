# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpacerItem, QVBoxLayout, QWidget)

class Ui_configForm(object):
    def setupUi(self, configForm):
        if not configForm.objectName():
            configForm.setObjectName(u"configForm")
        configForm.resize(822, 539)
        self.gridLayout = QGridLayout(configForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.configContainer = QWidget(configForm)
        self.configContainer.setObjectName(u"configContainer")
        self.gridLayout_2 = QGridLayout(self.configContainer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.optionsContainer = QWidget(self.configContainer)
        self.optionsContainer.setObjectName(u"optionsContainer")
        self.verticalLayout = QVBoxLayout(self.optionsContainer)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.optionsButtonsContainer = QWidget(self.optionsContainer)
        self.optionsButtonsContainer.setObjectName(u"optionsButtonsContainer")
        self.verticalLayout_2 = QVBoxLayout(self.optionsButtonsContainer)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.repeatLabelContainer = QWidget(self.optionsButtonsContainer)
        self.repeatLabelContainer.setObjectName(u"repeatLabelContainer")
        self.horizontalLayout_3 = QHBoxLayout(self.repeatLabelContainer)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.repeatButtonLabel = QLabel(self.repeatLabelContainer)
        self.repeatButtonLabel.setObjectName(u"repeatButtonLabel")
        font = QFont()
        font.setBold(True)
        self.repeatButtonLabel.setFont(font)

        self.horizontalLayout_3.addWidget(self.repeatButtonLabel)

        self.repeatHelperLabel = QLabel(self.repeatLabelContainer)
        self.repeatHelperLabel.setObjectName(u"repeatHelperLabel")
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(True)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.repeatHelperLabel.setFont(font1)
        self.repeatHelperLabel.setStyleSheet(u"")
        self.repeatHelperLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.repeatHelperLabel)


        self.verticalLayout_2.addWidget(self.repeatLabelContainer)

        self.repeatButtonContainer = QWidget(self.optionsButtonsContainer)
        self.repeatButtonContainer.setObjectName(u"repeatButtonContainer")
        self.horizontalLayout = QHBoxLayout(self.repeatButtonContainer)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.repeatOnButton = QRadioButton(self.repeatButtonContainer)
        self.repeatButtonGroup = QButtonGroup(configForm)
        self.repeatButtonGroup.setObjectName(u"repeatButtonGroup")
        self.repeatButtonGroup.addButton(self.repeatOnButton)
        self.repeatOnButton.setObjectName(u"repeatOnButton")
        self.repeatOnButton.setChecked(False)

        self.horizontalLayout.addWidget(self.repeatOnButton)

        self.repeatOffButton = QRadioButton(self.repeatButtonContainer)
        self.repeatButtonGroup.addButton(self.repeatOffButton)
        self.repeatOffButton.setObjectName(u"repeatOffButton")
        self.repeatOffButton.setChecked(True)

        self.horizontalLayout.addWidget(self.repeatOffButton)


        self.verticalLayout_2.addWidget(self.repeatButtonContainer)

        self.durationLabalContainer = QWidget(self.optionsButtonsContainer)
        self.durationLabalContainer.setObjectName(u"durationLabalContainer")
        self.horizontalLayout_4 = QHBoxLayout(self.durationLabalContainer)
        self.horizontalLayout_4.setSpacing(1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.durationLabel = QLabel(self.durationLabalContainer)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setFont(font)

        self.horizontalLayout_4.addWidget(self.durationLabel)

        self.durationHelperLabel = QLabel(self.durationLabalContainer)
        self.durationHelperLabel.setObjectName(u"durationHelperLabel")
        self.durationHelperLabel.setFont(font1)
        self.durationHelperLabel.setStyleSheet(u"")
        self.durationHelperLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.durationHelperLabel)


        self.verticalLayout_2.addWidget(self.durationLabalContainer)

        self.durationSliderContainer = QWidget(self.optionsButtonsContainer)
        self.durationSliderContainer.setObjectName(u"durationSliderContainer")
        self.durationSliderContainer.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(self.durationSliderContainer)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.zeroLabel = QLabel(self.durationSliderContainer)
        self.zeroLabel.setObjectName(u"zeroLabel")

        self.horizontalLayout_2.addWidget(self.zeroLabel)

        self.durationSlider = QSlider(self.durationSliderContainer)
        self.durationSlider.setObjectName(u"durationSlider")
        self.durationSlider.setMinimum(0)
        self.durationSlider.setMaximum(9)
        self.durationSlider.setValue(0)
        self.durationSlider.setSliderPosition(0)
        self.durationSlider.setOrientation(Qt.Orientation.Horizontal)
        self.durationSlider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.durationSlider.setTickInterval(1)

        self.horizontalLayout_2.addWidget(self.durationSlider)

        self.nineLabel = QLabel(self.durationSliderContainer)
        self.nineLabel.setObjectName(u"nineLabel")

        self.horizontalLayout_2.addWidget(self.nineLabel)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_2.addWidget(self.durationSliderContainer)

        self.exhaleButtonLabel = QLabel(self.optionsButtonsContainer)
        self.exhaleButtonLabel.setObjectName(u"exhaleButtonLabel")
        self.exhaleButtonLabel.setFont(font)

        self.verticalLayout_2.addWidget(self.exhaleButtonLabel)

        self.exhaleSelectButton = QPushButton(self.optionsButtonsContainer)
        self.exhaleSelectButton.setObjectName(u"exhaleSelectButton")

        self.verticalLayout_2.addWidget(self.exhaleSelectButton)

        self.inhaleButtonLabel = QLabel(self.optionsButtonsContainer)
        self.inhaleButtonLabel.setObjectName(u"inhaleButtonLabel")
        self.inhaleButtonLabel.setFont(font)

        self.verticalLayout_2.addWidget(self.inhaleButtonLabel)

        self.inhaleSelectButton = QPushButton(self.optionsButtonsContainer)
        self.inhaleSelectButton.setObjectName(u"inhaleSelectButton")

        self.verticalLayout_2.addWidget(self.inhaleSelectButton)

        self.confirmButton = QPushButton(self.optionsButtonsContainer)
        self.confirmButton.setObjectName(u"confirmButton")

        self.verticalLayout_2.addWidget(self.confirmButton)


        self.verticalLayout.addWidget(self.optionsButtonsContainer)

        self.verticalLayout.setStretch(0, 3)

        self.gridLayout_2.addWidget(self.optionsContainer, 0, 1, 1, 1)

        self.pressureActionContainer = QWidget(self.configContainer)
        self.pressureActionContainer.setObjectName(u"pressureActionContainer")
        self.verticalLayout_3 = QVBoxLayout(self.pressureActionContainer)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 1)
        self.slidersContainer = QWidget(self.pressureActionContainer)
        self.slidersContainer.setObjectName(u"slidersContainer")
        self.horizontalLayout_7 = QHBoxLayout(self.slidersContainer)
        self.horizontalLayout_7.setSpacing(5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.exhaleContainer = QWidget(self.slidersContainer)
        self.exhaleContainer.setObjectName(u"exhaleContainer")
        self.horizontalLayout_6 = QHBoxLayout(self.exhaleContainer)
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.exhaleIconLabel = QLabel(self.exhaleContainer)
        self.exhaleIconLabel.setObjectName(u"exhaleIconLabel")
        self.exhaleIconLabel.setMinimumSize(QSize(200, 200))
        self.exhaleIconLabel.setMaximumSize(QSize(200, 200))
        self.exhaleIconLabel.setPixmap(QPixmap(u"_internal/resources/icons/exhale.png"))
        self.exhaleIconLabel.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.exhaleIconLabel)

        self.exhaleSliderContainer = QWidget(self.exhaleContainer)
        self.exhaleSliderContainer.setObjectName(u"exhaleSliderContainer")
        self.verticalLayout_4 = QVBoxLayout(self.exhaleSliderContainer)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 489, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_6.addWidget(self.exhaleSliderContainer)


        self.horizontalLayout_7.addWidget(self.exhaleContainer)

        self.inhaleContainer = QWidget(self.slidersContainer)
        self.inhaleContainer.setObjectName(u"inhaleContainer")
        self.horizontalLayout_5 = QHBoxLayout(self.inhaleContainer)
        self.horizontalLayout_5.setSpacing(1)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.inhaleIconLabel = QLabel(self.inhaleContainer)
        self.inhaleIconLabel.setObjectName(u"inhaleIconLabel")
        self.inhaleIconLabel.setMinimumSize(QSize(200, 200))
        self.inhaleIconLabel.setMaximumSize(QSize(200, 200))
        self.inhaleIconLabel.setPixmap(QPixmap(u"_internal/resources/icons/inhale.png"))
        self.inhaleIconLabel.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.inhaleIconLabel)

        self.inhaleSliderContainer = QWidget(self.inhaleContainer)
        self.inhaleSliderContainer.setObjectName(u"inhaleSliderContainer")
        self.verticalLayout_5 = QVBoxLayout(self.inhaleSliderContainer)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 0, 0, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 489, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addWidget(self.inhaleSliderContainer)


        self.horizontalLayout_7.addWidget(self.inhaleContainer)


        self.verticalLayout_3.addWidget(self.slidersContainer)

        self.verticalLayout_3.setStretch(0, 1)

        self.gridLayout_2.addWidget(self.pressureActionContainer, 0, 0, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 3)

        self.gridLayout.addWidget(self.configContainer, 1, 0, 1, 1)


        self.retranslateUi(configForm)

        QMetaObject.connectSlotsByName(configForm)
    # setupUi

    def retranslateUi(self, configForm):
        configForm.setWindowTitle(QCoreApplication.translate("configForm", u"Form", None))
        self.repeatButtonLabel.setText(QCoreApplication.translate("configForm", u"Repetir", None))
#if QT_CONFIG(tooltip)
        self.repeatHelperLabel.setToolTip(QCoreApplication.translate("configForm", u"Quando ligado, a entrada configurada ser\u00e1 repetida m\u00faltiplas vezes enquanto o sensor estiver pressionado", u"ConfigScreenHelper"))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.repeatHelperLabel.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.repeatHelperLabel.setText(QCoreApplication.translate("configForm", u"?", None))
        self.repeatOnButton.setText(QCoreApplication.translate("configForm", u"Ligado", None))
        self.repeatOffButton.setText(QCoreApplication.translate("configForm", u"Desligado", None))
        self.durationLabel.setText(QCoreApplication.translate("configForm", u"Dura\u00e7\u00e3o (s)", None))
#if QT_CONFIG(tooltip)
        self.durationHelperLabel.setToolTip(QCoreApplication.translate("configForm", u"Quantos segundos de press\u00e3o cont\u00ednua s\u00e3o necess\u00e1rios para que o controle registre uma entrada", u"ConfigScreenHelper"))
#endif // QT_CONFIG(tooltip)
        self.durationHelperLabel.setText(QCoreApplication.translate("configForm", u"?", None))
        self.zeroLabel.setText(QCoreApplication.translate("configForm", u"0", None))
        self.nineLabel.setText(QCoreApplication.translate("configForm", u"9", None))
        self.exhaleButtonLabel.setText(QCoreApplication.translate("configForm", u"Tecla sopro", None))
#if QT_CONFIG(tooltip)
        self.exhaleSelectButton.setToolTip(QCoreApplication.translate("configForm", u"Seleciona a tecla que deseja associar \u00e0 combina\u00e7\u00e3o de dedos, caso j\u00e1 selecionada, apresenta a tecla escolhida", u"ConfigScreenHelper"))
#endif // QT_CONFIG(tooltip)
        self.exhaleSelectButton.setText(QCoreApplication.translate("configForm", u"Clique para selecionar", None))
        self.inhaleButtonLabel.setText(QCoreApplication.translate("configForm", u"Tecla suc\u00e7\u00e3o", None))
#if QT_CONFIG(tooltip)
        self.inhaleSelectButton.setToolTip(QCoreApplication.translate("configForm", u"Seleciona a tecla que deseja associar \u00e0 combina\u00e7\u00e3o de dedos, caso j\u00e1 selecionada, apresenta a tecla escolhida", u"ConfigScreenHelper"))
#endif // QT_CONFIG(tooltip)
        self.inhaleSelectButton.setText(QCoreApplication.translate("configForm", u"Clique para selecionar", None))
#if QT_CONFIG(tooltip)
        self.confirmButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.confirmButton.setText(QCoreApplication.translate("configForm", u"Confirmar", None))
        self.exhaleIconLabel.setText("")
        self.inhaleIconLabel.setText("")
    # retranslateUi

