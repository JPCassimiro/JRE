from ui.views.app_helper_modal_ui import Ui_appHelpDialog

from modules.desktop_services import DekstopServicesClass

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QCoreApplication, QEvent

from pathlib import Path

class AppHelperModel(QDialog):
    def __init__(self):
        
        super().__init__()

        self.string_list_components = [
            QCoreApplication.translate("AppHelperDialogText","Ajuda"),
            QCoreApplication.translate("AppHelperDialogText","<a href='_internal/manual/manual.html'>Manual de usuário<a/>"),#has to be updated on linguist too
        ]

        self.ui = Ui_appHelpDialog()
        self.ui.setupUi(self)

        #get ui elements
        self.manualLinkLabel = self.ui.manualLinkLabel

        #setup connections
        self.manualLinkLabel.linkActivated.connect(self.open_manual)

        self.setWindowModality(Qt.ApplicationModal)

        self.set_ui_text()

    def open_manual(self,filePath):
        self.file_path = Path(filePath)
        DekstopServicesClass().open_folder(self.file_path)

    def set_ui_text(self):
        self.setWindowTitle(self.string_list_components[0])
        self.manualLinkLabel.setText(self.string_list_components[1])
            
    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.string_list_components = [
                QCoreApplication.translate("AppHelperDialogText","Ajuda"),
                QCoreApplication.translate("AppHelperDialogText","<a href='_internal/manual/manual.html'>Manual de usuário<a/>"),#has to be updated on linguist too
            ]
            self.set_ui_text()
        return super().changeEvent(event)