from shared_ui_modules.modules.log_class import logger

from PySide6.QtCore import QObject

import json
from pathlib import Path

class JsonWriterClass(QObject):
    def __init__(self):
        super().__init__()
        
        self.base_path = Path("_internal/resources/latest_bindings")
        self.device_path = Path("_internal/resources/cached_devices")
        
    def write_bindings(self,bindingDict):
        try:
            if bindingDict is None:
                raise Exception(f"null bindingDict: {bindingDict}")

            self.base_path.mkdir(parents=True, exist_ok=True)
            json_file = self.base_path / f"user_bindings.json"
            
            dataArray = []
            
            for binding in bindingDict:
                data = {
                    "duration":f"{binding["duration"]}",
                    "key": f"{binding["key"]}",
                    "repeat": f"{binding["repeat"]}",
                    "action": f"{binding['action']}",
                    "pressure": f"{binding['pressure']}",
                }
                dataArray.append(data)

            data_str = json.dumps(dataArray, indent=4)
            with open(json_file, 'w+') as file:
                file.write(data_str)
                
            logger.info(f"Configuração escrita.")
        except Exception as e:
            logger.error(f"JsonWriterClass write_bindings error: {e}")
        
    def write_devices(self, deviceDict):
        try:
            if deviceDict is None:
                raise Exception(f"null deviceDict: {deviceDict}")

            self.device_path.mkdir(parents=True, exist_ok=True)
            json_file = self.device_path / f"cached_devices.json"

            logger.debug(f"write_devices deviceDict: {deviceDict["uuid"].toString()}")
        
            if json_file.exists():
                with open(json_file, 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            data[deviceDict["mac"]] = {
                "uuid": deviceDict["uuid"].toString(),
                "name": deviceDict["name"]
            }
            
            with open(json_file, 'w') as file:
                data_str = json.dumps(data)
                file.write(data_str)
        except Exception as e:
            logger.error(f"JsonWriterClass write_devices error: {e}")
            
    def read_json_file(self, file_path_str):
        try:
            if file_path_str is None:
                raise Exception(f"null file_path_str: {file_path_str}")

            path = Path(file_path_str)
            with open(path,"r") as f:
                data = json.load(f)
            
            return data
        except Exception as e:
            logger.error(f"JsonWriterClass read_json_file error: {e}")
            return None