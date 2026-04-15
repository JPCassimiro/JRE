from modules.log_class import logger

from PySide6.QtCore import QObject

import json
from pathlib import Path

class JsonWriterClass(QObject):
    def __init__(self):
        super().__init__()
        
        self.base_path = Path("_internal/resources/latest_bindings")
        
    def write_bindings(self,bindingDict):
        self.base_path.mkdir(parents=True, exist_ok=True)
        json_file = self.base_path / f"user_bindings.json"
        
        data = {
                "duration":f"{bindingDict["duration"]}",
                "key": f"{bindingDict["key"]}",
                "repeat": f"{bindingDict["repeat"]}",
                "action": f"{bindingDict['action']}",
                "pressure": f"{bindingDict['pressure']}",
            }

        data_str = json.dumps(data, indent=4)
        with open(json_file, 'w+') as file:
            file.write(data_str)
            
        logger.info(f"Configuração escrita.")
        
    