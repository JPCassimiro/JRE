from ui.model.stacked_widget_screens.connection_manager_model import ConnectionManagerModel
from ui.model.components.patient_widget_model import PatientWidgetModel
from ui.model.components.title_widget_model import TitleWidgetModel
from ui.model.stacked_widget_screens.config_widget_model import ConfigWidgetModel
from ui.model.stacked_widget_screens.calibration_widget_model import CalibrationWidgetModel
from ui.model.stacked_widget_screens.user_actions_widget_model import UserActionsModel
from ui.model.stacked_widget_screens.user_stats_model import UserStatsModel
from ui.model.dialogs.log_model import LogModel
from ui.model.dialogs.app_config_dialog_model import AppConfigModel
from ui.model.dialogs.app_helper_model import AppHelperModel
from ui.model.stacked_widget_screens.game_config_profile_model import GameProfileModel

from ui.views.main_window_ui import Ui_MainWindow

from PySide6.QtWidgets import QPushButton, QMainWindow, QApplication
from PySide6.QtCore import QEvent, QCoreApplication, Qt
from PySide6.QtGui import QPixmap

from modules.serial_communication import SerialCommClass
from modules.db_functions import DbClass
from modules.bluetooth_serial_communication import BtSerialComm

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #setup shared instances
        self.serialHandleClass = SerialCommClass()
        self.dbHandleClass = DbClass()
        self.logModel = LogModel()
        self.btSerialHandle = BtSerialComm()

        #setup translatable strings
        self.string_list_components = [
            "JRE"
        ]
        
        #set main windows
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(QCoreApplication.translate("MainMenuText", self.string_list_components[0]))

        
        #get logo label
        self.logoLabel = self.ui.logoLabel
        self.logoImg = QPixmap()
        if self.logoImg.load("_internal/resources/icons/main_menu_logo.png"):
            self.logoLabel.setMaximumHeight(64)
            self.logoLabel.setMaximumWidth(64)
            self.logoLabel.setMinimumHeight(64)
            self.logoLabel.setMinimumWidth(64)
            self.logoLabel.setPixmap(self.logoImg)
            self.logoLabel.setScaledContents(True)
        
        #get stackabledWidget
        self.stackedWidget = self.ui.stackedWidget
        
        #get container widgets
        self.patinetWidgetContainer = self.ui.patientWidget
        self.titletWidgetContainer = self.ui.titleWidget
        
        #get widgets
        # self.logger_widget = LoggerWidgetModel(self.serialHandleClass, self.logModel)
        self.connection_manager_widget = ConnectionManagerModel(self.serialHandleClass, self.logModel, self.btSerialHandle)
        self.patient_widget = PatientWidgetModel()
        self.title_widget = TitleWidgetModel()
        self.config_widget = ConfigWidgetModel(self.serialHandleClass,self.btSerialHandle, self.logModel)
        self.calibration_widget = CalibrationWidgetModel(self.serialHandleClass,self.logModel, self.btSerialHandle)
        self.user_actions_widget = UserActionsModel(self.dbHandleClass)
        self.user_stats_widget = UserStatsModel(self.dbHandleClass,self.serialHandleClass, self.btSerialHandle, self.logModel)
        self.side_menu = self.ui.sideMenu_2
        self.game_profile_widget = GameProfileModel(self.logModel,self.dbHandleClass, self.btSerialHandle)

        #setup config modal
        self.appConfigModal = AppConfigModel()
        
        #setup manual modal
        self.manual_modal = AppHelperModel()
        
        #setup signal connections
        self.calibration_widget.pValuesSignal.connect(self.handle_pValues_signal)
        self.user_actions_widget.therapistSelected.connect(self.therapist_select_handler)
        self.user_actions_widget.patientSelected.connect(self.patient_select_handler)
        self.user_actions_widget.assin_default_user()
        self.game_profile_widget.to_config.connect(self.to_config_signal_handle)
        
        #setup stackedWidget
        self.stackedWidget.insertWidget(0, self.connection_manager_widget)
        self.stackedWidget.insertWidget(1, self.config_widget)
        self.stackedWidget.insertWidget(2, self.calibration_widget)
        self.stackedWidget.insertWidget(3, self.user_actions_widget)
        self.stackedWidget.insertWidget(4, self.user_stats_widget)
        self.stackedWidget.insertWidget(5, self.game_profile_widget)
        
        #setups widgets on their containers
        self.patinetWidgetContainer.layout().addWidget(self.patient_widget)
        self.titletWidgetContainer.layout().addWidget(self.title_widget)

        #get buttons
        self.connectionMenuButton = self.ui.connectionMenuButton
        self.configButton = self.ui.configButton
        self.calibrationButton = self.ui.calibrationButton
        self.userActionsButton = self.ui.userActionsButton
        self.statsButton = self.ui.statsButton
        self.logModalButton = self.ui.logModalButton
        self.appConfigButton = self.ui.appConfigButton
        self.manualButton = self.ui.manualButton
        self.gameProfileButton = self.ui.gameProfileButton
        # self.gameProfileButton.hide()#!for now

        self.connectionMenuButton.setEnabled(False)#screen always starts at this widget
        
        #setup button connections
        self.connectionMenuButton.clicked.connect(self.connection_menu_button_handler)
        self.configButton.clicked.connect(self.config_menu_button_handler)
        self.calibrationButton.clicked.connect(self.calibration_menu_button_handler)
        self.userActionsButton.clicked.connect(self.user_menu_button_handler)
        self.statsButton.clicked.connect(self.stats_menu_button_handler)
        self.logModalButton.clicked.connect(self.log_button_handler)
        self.appConfigButton.clicked.connect(self.app_config_button_handler)
        self.manualButton.clicked.connect(self.app_manual_button_handler)
        self.gameProfileButton.clicked.connect(self.game_profile_button_handler)

        #button toggling connections
        self.calibration_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.calibrationButton))
        self.user_stats_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.statsButton))
        # self.logger_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.connectionMenuButton))
        self.connection_manager_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.connectionMenuButton))

        self.stackedWidget.setCurrentIndex(0)

    def connection_menu_button_handler(self):
        self.side_menu_button_toggler(self.connectionMenuButton)
        self.stackedWidget.setCurrentIndex(0)
        
    def config_menu_button_handler(self):
        self.side_menu_button_toggler(self.configButton)
        self.stackedWidget.setCurrentIndex(1)

    def calibration_menu_button_handler(self):
        self.side_menu_button_toggler(self.calibrationButton)
        self.stackedWidget.setCurrentIndex(2)     
        
    def stats_menu_button_handler(self):
        self.side_menu_button_toggler(self.statsButton)
        self.stackedWidget.setCurrentIndex(4)
        
    def user_menu_button_handler(self):
        self.side_menu_button_toggler(self.userActionsButton)
        self.stackedWidget.setCurrentIndex(3)     
    
    def game_profile_button_handler(self):
        self.side_menu_button_toggler(self.gameProfileButton)
        self.stackedWidget.setCurrentIndex(5)

    def handle_pValues_signal(self,array):
        self.config_widget.set_slider_max_value(array)

    def therapist_select_handler(self,infoDict):
        self.title_widget.info_dict = infoDict.copy()
        self.title_widget.update_fields()
        
    def patient_select_handler(self,infoDict):
        self.patient_widget.info_dict = infoDict.copy()
        self.patient_widget.update_fields()
        if "id" in infoDict:
            self.user_stats_widget.assing_user(infoDict["id"],infoDict["name"])
            self.config_widget.current_user = infoDict["id"]
            self.game_profile_widget.assing_user(infoDict["id"])
        
    def log_button_handler(self):
        self.logModel.open()

    # toggles side menu buttons accordingly
    def side_menu_button_toggler(self, clicked_button):
        for button in self.side_menu.findChildren(QPushButton):
            if button != clicked_button:
                button.setEnabled(True)
            else:
                clicked_button.setEnabled(False)
                
    def side_menu_button_disabler(self, state, clicked_button):
        for button in self.side_menu.findChildren(QPushButton):
            if button == clicked_button:
                clicked_button.setEnabled(False)
            else:
                button.setEnabled(state)
        self.appConfigButton.setEnabled(state)
        
    def app_config_button_handler(self):
        self.appConfigModal.show()

    def app_manual_button_handler(self):
        self.manual_modal.show()

    def to_config_signal_handle(self,config):
        self.config_widget.assing_card_values(config)
        self.stackedWidget.setCurrentIndex(1)
        self.side_menu_button_toggler(self.configButton)
        
    # event override    
    def closeEvent(self, event):
        modal_list = []
        modal_list.append(QApplication.activeModalWidget())
        if any(modal_list):
            for m in modal_list:
                m.close()
        return super().closeEvent(event)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
        return super().changeEvent(event)
        