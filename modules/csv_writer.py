from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox

from modules.log_class import logger

import csv
from pathlib import Path
from unidecode import unidecode

class CSVWriterClass(QObject):
    exportEnd = Signal(object)
    exportError = Signal(bool)
    
    def __init__(self, parent = None):
        super().__init__(parent)    

        self.csv_path = None
        
    def export_user_data(self, data):
        if data:
            try:
                self.csv_path = Path(f"dados_de_uso/paciente_{data["userId"]}_{unidecode(data["userName"][0][0]).replace(' ','_')}/{data["userHand"]}")#create folder structure
                self.csv_path.mkdir(parents=True, exist_ok=True)
                raw_data_path = self.csv_path / "Dados_brutos_por_sessao"
                statistical_data_path = self.csv_path / "Dados_estatisticos_por_sessao"
                summary_statistical_path = self.csv_path / "Resumo_dados_estatisticos"
                raw_data_path.mkdir(parents=True, exist_ok=True)
                statistical_data_path.mkdir(parents=True, exist_ok=True)
                summary_statistical_path.mkdir(parents=True, exist_ok=True)
                
                raw_data = [#list to struct
                    {
                        "action": row[0],
                        "pressure": f"{row[1]:.3f}",
                        "timestamp": row[2]
                    }
                    for row in data["raw_data"]
                ]
                
                raw_csv_file = raw_data_path / f"dados_brutos_{data["sessionDateString"][0][0].replace(':','-')}.csv"#create file for raw data
                with open(raw_csv_file, "w", newline = '') as file:#write on file
                    fieldNames = ["action","pressure","timestamp"]
                    writer = csv.DictWriter(file, fieldnames=fieldNames)
                    writer.writeheader()
                    writer.writerows(raw_data)

                session_data = [#list to struct
                    {
                        "max_exhale": f'{row[0][0]:.3f}',
                        "avg_exhale": f'{row[1][0]:.3f}',
                        "min_exhale": f'{row[2][0]:.3f}',
                        "total_presses_exhale": row[3][0],
                        "max_inhale": f'{row[0][1]:.3f}',
                        "avg_inhale": f'{row[1][1]:.3f}',
                        "min_inhale": f'{row[2][1]:.3f}',
                        "total_presses_inhale": row[3][1],
                    }
                    for row in data["session_data"]
                ]
                session_csv_file = statistical_data_path / f"dados_sessao_{data["sessionDateString"][0][0].replace(':','-')}.csv"#create file for session data
                with open(session_csv_file, "w", newline='') as file:#write session file
                    fieldNames = ["max_exhale","avg_exhale","min_exhale","total_presses_exhale",
                        "max_inhale","avg_inhale","min_inhale","total_presses_inhale"]
                    writer = csv.DictWriter(file,fieldNames)
                    writer.writeheader()
                    writer.writerows(session_data)
                    
                #headers - avg_press_finger x 4, timestamp
                
                pressure_data = data["summary_data"][:4]
                logger.debug(f"export_user_data pressure_data:{type(pressure_data[2])}")
                
                avg_press_summary = []

                actions = ["exhale", "inhale"]

                avg_press_summary = []

                for i, action in enumerate(actions):
                    for row in pressure_data[i]:
                        avg_press_summary.append({
                            "action": action,
                            "pressure": f'{row[1]:.3f}',
                            "timestamp": row[0]
                        })
                
                summary_avg_file = summary_statistical_path / f"resumo_dados_media_pressao.csv"#create file for session data
                with open(summary_avg_file, "w", newline='') as file:#write session file
                    fieldNames = ["action","pressure","timestamp"]
                    writer = csv.DictWriter(file,fieldNames)
                    writer.writeheader()
                    writer.writerows(avg_press_summary)

                avg_uses_array = data["summary_data"][4:6]
                total_avg_pressure_map = []
                for i, action in enumerate(actions):
                    press = avg_uses_array[0][i]
                    uses = avg_uses_array[1][i]

                    if press is not False and uses is False:
                        continue
                    
                    total_avg_pressure_map.append({
                        "action": action,
                        "total_avg_pressure": f"{press:.3f}" if press is not False else None,
                        "total_uses": uses if uses is not False else None
                    })
                summary_rest_file = summary_statistical_path / "Resumo_dados_media_e_total_de_usos.csv" 
                with open(summary_rest_file, "w", newline='') as file:
                    fieldNames = ["action","total_avg_pressure","total_uses"]
                    writer = csv.DictWriter(file,fieldNames)
                    writer.writeheader()
                    writer.writerows(total_avg_pressure_map)
            except Exception as e:
                logger.error(f"Erro ao exportar arquivos: {e}")
                self.exportError.emit(True)
            else:
                self.exportEnd.emit(self.csv_path)
        else:
            logger.error(f"Arquivos não encontrados")
            self.exportError.emit(True)

            
