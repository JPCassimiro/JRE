import sys, os
from pathlib import Path

from ui import main_menu
from modules import log_class

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings, QTranslator
from PySide6.QtGui import QIcon

try:
    from ctypes import windll  
    app_id = 'utfpr.jhrm.release.opensource'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except ImportError:
    pass

def init_settings(path, app):
    settings = QSettings(path, QSettings.IniFormat)
    language = settings.value("language")
    print(f"init_settings - language: {language} type: {type(language)}")
    app.translator = QTranslator()
    if language and language != "None":
        if app.translator.load(language):
            # print(f"init_settings res: {res}")
            app.installTranslator(app.translator)
        

def main():
    base_path_config = Path("_internal/resources/config/config.ini")

    try:
        app = QApplication(sys.argv)
        init_settings(str(base_path_config),app)
        window = main_menu.MainMenuWindow()
        window.show()

        main_qss_path = Path(__file__).parent / "ui" / "qss" / "main.qss"
        with open(main_qss_path,'r') as f:
            _style = f.read()
            app.setStyleSheet(_style)

        app.setWindowIcon(QIcon("_internal/resources/icons/logo.ico"))
            
        app.exec()
    except Exception as e:
        log_class.logger.exception(f"Erro na execução do Main\nErro: {e}")


if __name__ == "__main__":
    main()