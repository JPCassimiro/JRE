from shared_ui_modules.ui.main_menu import SharedMainMenuWindow

from ui.model.stacked_widget_screens.connection_manager_model import ConnectionManagerModel
from shared_ui_modules.ui.model.components.patient_widget_model import SharedPatientWidgetModel
from ui.model.components.title_widget_model import TitleWidgetModel
from ui.model.stacked_widget_screens.config_widget_model import ConfigWidgetModel
from ui.model.stacked_widget_screens.calibration_widget_model import CalibrationWidgetModel
from ui.model.stacked_widget_screens.user_actions_widget_model import UserActionsModel
from ui.model.stacked_widget_screens.user_stats_model import UserStatsModel
from ui.model.stacked_widget_screens.game_config_profile_model import GameProfileModel
from shared_ui_modules.ui.model.dialogs.log_model import SharedLogModel
from ui.model.dialogs.app_helper_model import AppHelperModule
from ui.model.dialogs.app_config_dialog_model import AppConfigDialogModel

from ui.views.main_window_ui import Ui_MainWindow

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPixmap

from modules.db_functions import DbClass
from modules.bluetooth_serial_communication import BtSerialComm
from shared_ui_modules.modules.log_class import logger

#!before new release
    #!change config.init current version on app_config_dialog_model
    #!change current version on inital log on main.py
    #!comment fake_data_test on SharedDataCollectorClass

class MainMenuWindow(SharedMainMenuWindow):
    def __init__(self):
        super().__init__()
        
        #setup shared instances
        self.dbHandleClass = DbClass()
        self.btSerialHandle = BtSerialComm()
        self.logModel = SharedLogModel(self.btSerialHandle)

            
        #set main windows
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("JRE")
        
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
        # self.logger_widget = LoggerWidgetModel( self.logModel)
        self.connection_manager_widget = ConnectionManagerModel( self.logModel, self.btSerialHandle)
        self.patient_widget = SharedPatientWidgetModel()
        self.title_widget = TitleWidgetModel()
        self.config_widget = ConfigWidgetModel(self.btSerialHandle, self.logModel)
        self.calibration_widget = CalibrationWidgetModel(self.logModel, self.btSerialHandle)
        self.user_actions_widget = UserActionsModel(self.dbHandleClass,self.logModel)
        self.user_stats_widget = UserStatsModel(self.dbHandleClass, self.btSerialHandle, self.logModel)
        self.side_menu = self.ui.sideMenu_2
        self.game_profile_widget = GameProfileModel(self.logModel,self.dbHandleClass, self.btSerialHandle)

        #setup config modal
        self.appConfigModal = AppConfigDialogModel()
        
        #setup manual modal
        self.manual_modal = AppHelperModule()
        
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
        self.gameProfileButton.clicked.connect(self.game_profile_button_handler)

        #button toggling connections
        self.calibration_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.calibrationButton))
        self.user_stats_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.statsButton))
        # self.logger_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.connectionMenuButton))
        self.connection_manager_widget.sideMenuDisableSignal.connect(lambda state: self.side_menu_button_disabler(state, self.connectionMenuButton))

        self.stackedWidget.setCurrentIndex(0)

        self.initialize_module()

    def connection_menu_button_handler(self):
        try:    
            self.side_menu_button_toggler(self.connectionMenuButton)
            self.stackedWidget.setCurrentIndex(0)
        except Exception as e:
            logger.error(f"MainMenuWindow connection_menu_button_handler error: {e}")
        
    def config_menu_button_handler(self):
        try:    
            self.side_menu_button_toggler(self.configButton)
            self.stackedWidget.setCurrentIndex(1)
        except Exception as e:
            logger.error(f"MainMenuWindow config_menu_button_handler error: {e}")

    def calibration_menu_button_handler(self):
        try:    
            self.side_menu_button_toggler(self.calibrationButton)
            self.stackedWidget.setCurrentIndex(2)     
        except Exception as e:
            logger.error(f"MainMenuWindow calibration_menu_button_handler error: {e}")
        
    def stats_menu_button_handler(self):
        try:    
            self.side_menu_button_toggler(self.statsButton)
            self.stackedWidget.setCurrentIndex(4)
        except Exception as e:
            logger.error(f"MainMenuWindow stats_menu_button_handler error: {e}")
        
    def user_menu_button_handler(self):
        try:    
            self.side_menu_button_toggler(self.userActionsButton)
            self.stackedWidget.setCurrentIndex(3)     
        except Exception as e:
            logger.error(f"MainMenuWindow user_menu_button_handler error: {e}")
    
    def game_profile_button_handler(self):
        try:    
            self.side_menu_button_toggler(self.gameProfileButton)
            self.stackedWidget.setCurrentIndex(5)
        except Exception as e:
            logger.error(f"MainMenuWindow game_profile_button_handler error: {e}")

    def handle_pValues_signal(self,array):
        try:
            self.config_widget.set_slider_max_value(array)
        except Exception as e:
            logger.error(f"MainMenuWindow handle_pValues_signal error: {e}")