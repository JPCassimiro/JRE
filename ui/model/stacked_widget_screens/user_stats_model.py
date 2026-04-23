from ui.views.user_stats_ui import Ui_useStatisticsForm
from modules.use_data_collector import DataCollectorClass
from modules.csv_writer import CSVWriterClass
from modules.desktop_services import DekstopServicesClass

from PySide6.QtWidgets import QWidget, QPushButton, QRadioButton, QMessageBox
from modules.log_class import logger
from PySide6.QtCore import Signal, Qt, QCoreApplication, QEvent

import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from pathlib import Path
from unidecode import unidecode

class UserStatsModel(QWidget):

    sideMenuDisableSignal = Signal(bool)

    def __init__(self, dbHandleClass, SerialCommClass, btSerialHandle, LogModel):
        super().__init__()

        #ui setup
        self.ui = Ui_useStatisticsForm()
        self.ui.setupUi(self)
        
        #modules setup
        self.dataCollectorHandler = DataCollectorClass(dbHandleClass, SerialCommClass, btSerialHandle, LogModel)
        self.dbHandleClass = dbHandleClass
        self.csvWriter = CSVWriterClass()
        
        #variables setup
        self.current_user = False
        self.latest_session = False
        self.current_user_name = ""

        #get ui elements
        self.startListening = self.ui.startListening
        self.stopListening = self.ui.stopListening
        self.sessionComboBox = self.ui.sessionComboBox
        self.timelapseLabel = self.ui.timelapseLabel
        self.statsTabWidget = self.ui.statsTabWidget
        self.countSession = self.ui.countSession
        self.avgSessionTime = self.ui.avgSessionTime
        self.newSessionButton = self.ui.newSessionButton
        self.deleteSessionButton = self.ui.deleteSessionButton
        self.exportSessionCSVButton = self.ui.exportSessioCSVButton
        self.exportSessionImageButton = self.ui.exportSessionImageButton

        #ui element setup
        self.timelapse = "00:00:00"
        self.sessionCount = "0"
        self.avgTimelapse = "00:00:00"
        self.timelapseLabel.setText(self.timelapse)
        self.countSession.setText(self.sessionCount)
        self.avgSessionTime.setText(self.avgTimelapse)
        
        self.startListening.setEnabled(False)
        self.stopListening.setEnabled(False)
        
        #connections setup
        self.startListening.clicked.connect(self.start_button_handler)
        self.stopListening.clicked.connect(self.stop_button_handler)
        self.sessionComboBox.currentIndexChanged.connect(self.comboBox_change_handler)
        self.statsTabWidget.tabBarClicked.connect(self.update_summary_charts)
        self.newSessionButton.clicked.connect(self.new_session_button_handler)
        self.deleteSessionButton.clicked.connect(self.delete_session_handler)
        self.exportSessionCSVButton.clicked.connect(self.export_session_handler)
        self.csvWriter.exportEnd.connect(self.end_export_handle)
        self.csvWriter.exportError.connect(self.error_export_handle)
        self.dataCollectorHandler.errorOcurred.connect(self.data_collection_error_handle)
        self.exportSessionImageButton.clicked.connect(self.export_as_image_handler)

        #create charts
        self.session_chart_layout_widget = None
        self.summary_chart_layout_widget = None
        self.create_charts()
        
    def export_as_image_handler(self):
        if self.sessionComboBox.currentIndex() >= 0:
            try:
                #exporter for current session
                exporter = pg.exporters.ImageExporter(self.session_chart_layout_widget.scene())

                #file path
                #get patient name form db
                q = f"""select name from patient where patient.id = ?;"""
                patient_name = self.dbHandleClass.execute_single_query(q,[self.current_user])

                #create folder structure
                folder_path = Path(f"dados_de_uso/paciente_{self.current_user}_{unidecode(patient_name[0][0].replace(' ','_'))}")
                folder_path.mkdir(parents=True, exist_ok=True)

                q = f"""SELECT datetime(session_date,'-03:00')
                            FROM session
                            WHERE id = ?
                            AND patient_id = ?;"""
                session_date_string = self.dbHandleClass.execute_single_query(q,[self.sessionComboBox.currentData(),self.current_user])

                #save file 1
                file_path = folder_path / f"sessao_{session_date_string[0][0].replace(':','-')}.png"
                exporter.export(str(file_path))
                
                #file 2, summary
                exporter = pg.exporters.ImageExporter(self.summary_chart_layout_widget.scene())

                file_path = folder_path /  "resumo.png"
                
                exporter.export(str(file_path))
                
            except Exception as e:
                logger.debug(f"Erro na exportação: {e}")
                self.error_export_handle()
            else:
                self.end_export_handle(folder_path)
        else:
            logger.error("Selecione uma sessão")
            warning = QMessageBox(self)
            warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
            warning.setText(QCoreApplication.translate("WarningText", "Selecione uma sessão"))
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()

    def data_collection_error_handle(self):
        warning = QMessageBox(self)
        warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
        warning.setText(QCoreApplication.translate("WarningText", "Erro na coleta, dados podem ter sido perdidos"))
        warning.setWindowModality(Qt.ApplicationModal)
        warning.show()
        if self.dataCollectorHandler.start_watch == True:
            self.stop_button_handler()
        # elif self.dataCollectorHandler.start_watch = False
            # self.stop_button_handler()

    
    def create_charts(self):
        #setup text to be translated
        
        #graph text
        self.string_list_graphs = [
            QCoreApplication.translate("GraphText","Sopro"),
            QCoreApplication.translate("GraphText","Sucção"),
            QCoreApplication.translate("GraphText","Estatisticas de pressão"),
            QCoreApplication.translate("GraphText","Progresso de pressão por função respiratória"),
            QCoreApplication.translate("GraphText","Média"),
            QCoreApplication.translate("GraphText","Maxima"),
            QCoreApplication.translate("GraphText","Mínima"),
            QCoreApplication.translate("GraphText","Média por função respiratória"),
            QCoreApplication.translate("GraphText","Uso de função respiratória"),
            QCoreApplication.translate("GraphText","Sessão"),
            QCoreApplication.translate("GraphText","Paciente: {user}"),
            QCoreApplication.translate("GraphText","Total de uso por função respiratória"),
            
        ]

        #dialog text
        self.string_list_dialog = [
            QCoreApplication.translate("UserStatsDialogText","Confirmar"),
            QCoreApplication.translate("UserStatsDialogText","Cancelar"),
            QCoreApplication.translate("UserStatsDialogText","Deseja excluir a sessão selecionada?"),
            QCoreApplication.translate("UserStatsDialogText","Aviso"),
            QCoreApplication.translate("UserStatsDialogText","Sucesso"),
            QCoreApplication.translate("UserStatsDialogText","Sessão de id {id}, do usuário {user} removida")
        ]
        
        #session chart widget        
        pg.setConfigOption('background', '#F5F5F5')
        pg.setConfigOption('foreground', 'black')
        self.session_chart_layout_widget =  pg.GraphicsLayoutWidget()
        self.ui.sessionChartContainer.layout().addWidget(self.session_chart_layout_widget)
        x_range = np.array([0,1])
        self.action_name_labels = [(x_range[0],self.string_list_graphs[0]),(x_range[1],self.string_list_graphs[1])]
        
        #create session patient name label       
        labelText = self.string_list_graphs[10].format(user = self.current_user_name)
        self.sessionNameLabel = pg.LabelItem(labelText)
        
        self.session_chart_layout_widget.addItem(self.sessionNameLabel, col = 2, row = 2)

        #avarage pressure by action chart
        self.avg_pressure = [0,0]
        self.avg_chart = pg.BarGraphItem(x= x_range,height=self.avg_pressure,width = 0.2,brush="#F89E59")
        
        #max pressure by action chart
        self.max_pressure = [0,0]
        self.max_chart = pg.BarGraphItem(x= x_range+0.2,height=self.max_pressure,width = 0.2,brush="#F37F27")
        
        #min pressure by action chart
        self.min_pressure = [0,0]
        self.min_chart = pg.BarGraphItem(x= x_range-0.2,height=self.max_pressure,width = 0.2,brush="#F6E1A4")
        
        #times action has been used
        self.times_pressed = [0,0]
        self.times_used_chart = pg.BarGraphItem(x= x_range,height=self.times_pressed,width = 0.3,brush="#F89E59")

        #add charts to layout
        self.plot_item_pressure = self.session_chart_layout_widget.addPlot(title = self.string_list_graphs[2], col = 1, row = 1)
        self.plot_item_pressure.setMouseEnabled(x=False,y=False)
        self.plot_item_pressure.addItem(self.avg_chart)
        self.plot_item_pressure.addItem(self.min_chart)
        self.plot_item_pressure.addItem(self.max_chart)
        self.plot_item_pressure.getAxis('bottom').setTicks([self.action_name_labels])
        self.plot_item_pressure.getAxis('left').setLabel(text = self.string_list_graphs[3], units = "kPa")
        
        #legend pressure chart session
        self.legendSessionPressure = pg.LegendItem(colCount = 3)
        self.legendSessionPressure.addItem(self.avg_chart,self.string_list_graphs[4])
        self.legendSessionPressure.addItem(self.max_chart,self.string_list_graphs[5])
        self.legendSessionPressure.addItem(self.min_chart,self.string_list_graphs[6])
        self.session_chart_layout_widget.addItem(self.legendSessionPressure, col = 1, row = 2)
        self.legendSessionPressure.setParentItem(self.session_chart_layout_widget.layout())
        
        #action use times session
        self.plot_item_times_used = self.session_chart_layout_widget.addPlot(title = self.string_list_graphs[8], col = 2, row = 1)
        self.plot_item_times_used.setMouseEnabled(x=False,y=False)
        self.plot_item_times_used.addItem(self.times_used_chart)
        self.plot_item_times_used.getAxis('bottom').setTicks([self.action_name_labels])
        self.plot_item_times_used.getAxis('left').setLabel(text=self.string_list_graphs[11])
        self.plot_item_times_used.getAxis('left').setStyle(maxTickLevel=0)
        
        #summary chart widget
        self.summary_chart_layout_widget = pg.GraphicsLayoutWidget()
        self.ui.summaryChartContainer.layout().addWidget(self.summary_chart_layout_widget)

        #add patient name label
        self.summaryNameLabel = pg.LabelItem(labelText)
        self.summary_chart_layout_widget.addItem(self.summaryNameLabel, col = 2, row = 2)

        #create line chart
        self.exhale_info_array = [[1,2],[1,2]]
        self.inhale_info_array = [[1,2],[1,2]]

        self.plot_item_avg_line = self.summary_chart_layout_widget.addPlot(col = 1, row = 1)
        self.plot_item_avg_line.getAxis('bottom').setLabel(self.string_list_graphs[9])
        self.plot_item_avg_line.getAxis('left').setLabel(self.string_list_graphs[3], units = "kPa")
        self.plot_item_avg_line.showGrid(y = True,x = True)

        #create lines
        self.exhale_line = self.plot_item_avg_line.plot(self.exhale_info_array[0],self.exhale_info_array[1],pen ='r')
        self.inhale_line = self.plot_item_avg_line.plot(self.inhale_info_array[0],self.inhale_info_array
                                                        [1],pen ='g')
            
        #line chart legend
        self.avg_line_legend = pg.LegendItem(colCount = 2)
        self.avg_line_legend.addItem(self.exhale_line, name = self.string_list_graphs[0])
        self.avg_line_legend.addItem(self.inhale_line, name = self.string_list_graphs[1])
        self.summary_chart_layout_widget.addItem(self.avg_line_legend, col = 1, row = 2)
        self.avg_line_legend.setParentItem(self.summary_chart_layout_widget.layout())

        #avg bar chart 
        self.plot_item_avg_bar = self.summary_chart_layout_widget.addPlot(col = 2, row = 1)
        self.avg_pressure_summary = [0,0]
        self.avg_chart_summary = pg.BarGraphItem(x= x_range,height=self.avg_pressure_summary,width = 0.2,brush="#F89E59")
        self.plot_item_avg_bar.addItem(self.avg_chart_summary)
        self.plot_item_avg_bar.getAxis('bottom').setTicks([self.action_name_labels])
        self.plot_item_avg_bar.getAxis('left').setLabel(text=self.string_list_graphs[7], units = "kPa")
        self.plot_item_avg_bar.setMouseEnabled(x=False, y=False)
        
        #total times used chart
        self.plot_item_total_uses = self.summary_chart_layout_widget.addPlot(col = 3, row = 1)
        self.total_uses_summary = [0,0]
        self.uses_chart_summary = pg.BarGraphItem(x= x_range,height=self.total_uses_summary,width = 0.2,brush="#F89E59")
        self.plot_item_total_uses.addItem(self.uses_chart_summary)
        self.plot_item_total_uses.getAxis('bottom').setTicks([self.action_name_labels])
        self.plot_item_total_uses.getAxis('left').setLabel(text=self.string_list_graphs[11])
        self.plot_item_total_uses.setMouseEnabled(x=False, y=False)
        

    def end_export_handle(self, folder_path = None):
        warning = QMessageBox(self)
        warning.setWindowTitle(QCoreApplication.translate("WarningText", "Sucesso"))
        warning.setText(QCoreApplication.translate("WarningText", "Exportação realizada com sucesso. A pasta criada será aberta."))
        warning.setWindowModality(Qt.ApplicationModal)
        warning.show()
        if folder_path:
            DekstopServicesClass().open_folder(folder_path)


    def error_export_handle(self):
        warning = QMessageBox(self)
        warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
        warning.setText(QCoreApplication.translate("WarningText", "Erro na exportação"))
        warning.setWindowModality(Qt.ApplicationModal)
        warning.show()

    def export_session_handler(self):
        #get user session data
        if self.sessionComboBox.currentIndex() >= 0:
            q = f""" 
                    SELECT 
                        u.action,
                        u.pressure,
                        datetime(u.timestamp,'-03:00')
                    FROM use_data u
                    JOIN session s ON u.session_id = s.id
                    WHERE s.patient_id = ?
                    AND s.id = ?;"""
            use_data = self.dbHandleClass.execute_single_query(q,[self.current_user,self.sessionComboBox.currentData()])

            q = f"""SELECT datetime(session_date,'-03:00')
                    FROM session
                    WHERE id = ?
                    AND patient_id = ?;"""
            session_date_string = self.dbHandleClass.execute_single_query(q,[self.sessionComboBox.currentData(),self.current_user])

            q = f"""select name from patient where patient.id = ?;"""
            patient_name = self.dbHandleClass.execute_single_query(q,[self.current_user])
            
            q = f"""
                SELECT DISTINCT s.id, datetime(s.session_date,'-03:00')
                FROM session s
                JOIN use_data u ON u.session_id = s.id
                WHERE s.patient_id = ?
                ORDER BY s.session_date;"""
            session = self.dbHandleClass.execute_single_query(q,[self.current_user])
            session_map = {session_id: timestamp for session_id, timestamp in session}
            
            ids, values = (self.exhale_info_array + [[], []])[:2]
            
            exhale_map = [
                (session_map.get(session_id), value)
                for session_id, value in zip(ids, values)
                if session_id in session_map
            ]
            
            ids, values = (self.inhale_info_array + [[], []])[:2]
            inhale_map = [
                (session_map.get(session_id), value)
                for session_id, value in zip(ids, values)
                if session_id in session_map
            ]
            
            data_dict = {
                "userId": self.current_user,
                "userName": patient_name,
                "sessionDateString": session_date_string,
                "raw_data": use_data,
                "session_data": [[self.max_pressure,self.avg_pressure,self.min_pressure,self.times_pressed]],
                "summary_data": [exhale_map,inhale_map,self.avg_pressure_summary,self.total_uses_summary]
            }
            self.csvWriter.export_user_data(data_dict)
        else:
            logger.error("Selecione uma sessão")
            warning = QMessageBox(self)
            warning.setWindowTitle(QCoreApplication.translate("WarningText", "Erro"))
            warning.setText(QCoreApplication.translate("WarningText", "Selecione uma sessão"))
            warning.setWindowModality(Qt.ApplicationModal)
            warning.show()
        
    def delete_charts(self):
        self.summary_chart_layout_widget.deleteLater()
        self.session_chart_layout_widget.deleteLater()
        # self.ui.sessionChartContainer.layout().removeWidget(self.session_chart_layout_widget)
        # self.ui.summaryChartContainer.layout().removeWidget(self.summary_chart_layout_widget)
        
    def delete_session_handler(self):
        def on_accept():
            current_index = self.sessionComboBox.currentData()
            q = f"""delete from session where id = ? and patient_id = ? returning id;"""
            res = self.dbHandleClass.execute_single_query(q,[current_index,self.current_user])
            self.populate_comboBox()
            if res:
                deletionMessage = QMessageBox(self)
                deletionMessage.setWindowTitle(self.string_list_dialog[4])
                message = self.string_list_dialog[5]
                message = message.format(id = res[0][0], user = self.current_user)
                deletionMessage.setText(message)
                deletionMessage.setWindowModality(Qt.ApplicationModal)
                deletionMessage.show()

        deletionDialog = QMessageBox(self)
        deletionDialog.setWindowTitle(self.string_list_dialog[3])
        deletionDialog.setText(self.string_list_dialog[2])
        deletionDialog.setWindowModality(Qt.ApplicationModal)
        deletionDialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        yes_button = deletionDialog.button(QMessageBox.Yes)
        no_button = deletionDialog.button(QMessageBox.No)
        yes_button.setText(self.string_list_dialog[0])
        no_button.setText(self.string_list_dialog[1])
        deletionDialog.buttonClicked.connect(lambda btn: on_accept() if btn == yes_button else None)
        deletionDialog.show()
    
    def stop_button_handler(self):
        self.dataCollectorHandler.stop_data_collection()
        self.button_toggler(self.stopListening)
        self.update_session_chart_value()
        self.update_summary_charts()

        
    def comboBox_change_handler(self):
        current_index = self.sessionComboBox.currentData()
        if (current_index != self.latest_session):
            self.startListening.setEnabled(False)
        else:
            self.startListening.setEnabled(True)
        self.update_session_chart_value()  
        self.update_summary_charts()
    
    def start_button_handler(self):
        self.dataCollectorHandler.start_watch = True
        self.button_toggler(self.startListening)
        
    def new_session_button_handler(self):
        session_id = self.create_session()
        if session_id:
            self.populate_comboBox()

    def assing_user(self,user_index,user_name):
        self.current_user = user_index
        self.dataCollectorHandler.current_user_index = self.current_user
        self.current_user_name = user_name
        self.populate_comboBox()

    def create_session(self):
        q = f"""insert into session (patient_id, session_date) values (?,datetime(current_timestamp,'localtime')) returning patient_id,id;"""
        res = self.dbHandleClass.execute_single_query(q,[self.current_user])
        if res:
            logger.debug(f"Seção criada para o usuário {res[0][0]}")
            return res[0][1]
        else:
            return False

    def get_summary_chart_value(self):
        qAvg = f"""SELECT 
            s.id AS session_id,
            u.action,
            AVG(u.pressure) AS avg_pressure
        FROM 
            use_data u
        JOIN 
            session s ON u.session_id = s.id
        JOIN 
            patient p ON s.patient_id = p.id
        WHERE 
            p.id = ?
        GROUP BY 
            s.session_date, u.action
        ORDER BY 
            s.session_date;"""
        qAvgTotal = f"""SELECT 
            u.action,
            AVG(u.pressure) AS avg_pressure
        FROM 
            use_data u
        JOIN 
            session s ON u.session_id = s.id
        JOIN 
            patient p ON s.patient_id = p.id
        WHERE 
            p.id = ?
        GROUP BY 
            u.action
        ORDER BY 
            u.action;"""
        qTotalCount = f"""SELECT 
            u.action,
            COUNT(*) AS total_actions_taken
        FROM 
            use_data u
        JOIN 
            session s ON u.session_id = s.id
        JOIN 
            patient p ON s.patient_id = p.id
        WHERE 
            p.id = ?
        GROUP BY 
            u.action
        ORDER BY 
            u.action;"""
        qSessionCount = f"select count(id) from session where patient_id = ?;"
        qAvgTimelapse = f"""SELECT
            printf('%02d:%02d:%02d',
                AVG(duration_seconds) / 3600,                
                (AVG(duration_seconds) % 3600) / 60,       
                AVG(duration_seconds) % 60               
            ) AS avg_duration_hhmmss
        FROM (
            SELECT
                CAST((JULIANDAY(MAX(use_data.timestamp)) - JULIANDAY(MIN(use_data.timestamp))) * 86400 AS INTEGER) AS duration_seconds
            FROM
                session
            JOIN
                use_data ON session.id = use_data.session_id
            WHERE
                session.patient_id = ?
            GROUP BY
                session.id
        );"""
        resAvg = self.dbHandleClass.execute_single_query(qAvg,[self.current_user])
        resAvgTotal = self.dbHandleClass.execute_single_query(qAvgTotal,[self.current_user])
        resTotalCount = self.dbHandleClass.execute_single_query(qTotalCount,[self.current_user])
        resSessionCount = self.dbHandleClass.execute_single_query(qSessionCount,[self.current_user])
        resAvgTimelapse = self.dbHandleClass.execute_single_query(qAvgTimelapse,[self.current_user])
        
        if resAvg and resAvgTotal and resTotalCount and resSessionCount and resAvgTimelapse:
            exhale_array = [[],[]]
            inhale_array = [[],[]]
            total_count = [False,False]
            avg_total = [False,False]
            sessionCount = False
            avgTimelapse = False
            
            ocurance_counter = [1,1]
            
            for i,t in enumerate(resAvg):
                if t[1] == "exhale":#i,t[2]/10
                    exhale_array[0].append(ocurance_counter[0])
                    exhale_array[1].append(t[2]/10)
                    ocurance_counter[0] = ocurance_counter[0]+1
                if t[1] == "inhale":
                    inhale_array[0].append(ocurance_counter[1])
                    inhale_array[1].append(t[2]/10)
                    ocurance_counter[1] = ocurance_counter[1]+1

            for t in resAvgTotal:
                if t[0] == 'exhale':
                    avg_total[0] = t[1]/10
                elif t[0] == 'inhale':
                    avg_total[1] = t[1]/10
            for t in resTotalCount:
                if t[0] == 'exhale':
                    total_count[0] = t[1]
                elif t[0] == 'inhale':
                    total_count[1] = t[1]
            sessionCount = resSessionCount[0][0]
            avgTimelapse = resAvgTimelapse[0][0]

            return exhale_array, inhale_array, total_count, avg_total, sessionCount, avgTimelapse
        
        else:
            return False,False,False,False,False,False        
                
    def update_summary_charts(self):
        exhale_array, inhale_array, total_count, avg_total, sessionCount, avgTimelapse = self.get_summary_chart_value()
        if exhale_array and inhale_array and total_count and avg_total and sessionCount and avgTimelapse:
            self.exhale_info_array = exhale_array
            self.inhale_info_array = inhale_array
            self.avg_pressure_summary = avg_total
            self.total_uses_summary = total_count
            self.sessionCount = sessionCount
            self.avgTimelapse = avgTimelapse
        else:
            self.exhale_info_array = [[1,2],[1,1]]
            self.inhale_info_array = [[1,2],[1,1]]
            self.avg_pressure_summary = [0,0]
            self.total_uses_summary = [0,0]
            self.sessionCount = "0"
            self.avgTimelapse = "00:00:00"
            
        self.avg_chart_summary.setOpts(height = self.avg_pressure_summary) 
        self.uses_chart_summary.setOpts(height = self.total_uses_summary)
        self.exhale_line.setData(self.exhale_info_array[0],self.exhale_info_array[1])
        self.inhale_line.setData(self.inhale_info_array[0],self.inhale_info_array[1])
        self.countSession.setText(str(self.sessionCount))
        self.avgSessionTime.setText(self.avgTimelapse)
        self.summaryNameLabel.setText(self.string_list_graphs[10].format(user = self.current_user_name))

    def get_session_chart_value(self):
        self.sessionComboBox.setEnabled(False)
        qCount = f"select action, COUNT(*) AS count from use_data where session_id = ? GROUP BY action;"
        qPres = f"SELECT action, MAX(pressure) AS max_pressure, MIN(pressure) AS min_pressure, AVG(pressure) AS avg_pressure FROM use_data where session_id = ? group by action;"
        qTimelapse = f"""SELECT 
            session_id,
            printf('%02d:%02d:%02d',
                duration_seconds / 3600,
                (duration_seconds % 3600) / 60,
                duration_seconds % 60
            ) AS duration_hms
        FROM (
            SELECT 
                session_id,
                CAST((strftime('%s', MAX(timestamp)) - strftime('%s', MIN(timestamp))) AS INTEGER) AS duration_seconds
            FROM use_data
            where session_id = ?);"""
        presRes = self.dbHandleClass.execute_single_query(qPres,[self.sessionComboBox.currentData()])
        countRes = self.dbHandleClass.execute_single_query(qCount,[self.sessionComboBox.currentData()])
        timelapseRes = self.dbHandleClass.execute_single_query(qTimelapse,[self.sessionComboBox.currentData()])
        if presRes and countRes and timelapseRes:
            max_press_array = [None,None]
            min_press_array = [None,None]
            avg_press_array = [None,None]
            action_count_array = [None,None]
            for t in presRes:
                if t[0] == 'exhale':
                    max_press_array[0] = t[1]/10
                    min_press_array[0] = t[2]/10
                    avg_press_array[0] = t[3]/10
                elif t[0] == 'inhale':
                    max_press_array[1] = t[1]/10
                    min_press_array[1] = t[2]/10
                    avg_press_array[1] = t[3]/10
            for t in countRes:
                if t[0] == 'exhale':
                    action_count_array[0] = t[1]
                elif t[0] == 'inhale':
                    action_count_array[1] = t[1]

            self.sessionComboBox.setEnabled(True)
            return  max_press_array, min_press_array, avg_press_array, action_count_array, timelapseRes

        else:
            self.sessionComboBox.setEnabled(True)
            return False,False,False,False,False

    def update_session_chart_value(self):
        max_press_array, min_press_array, avg_press_array, action_count_array, timelapse = self.get_session_chart_value()
        if max_press_array and min_press_array and avg_press_array and action_count_array and timelapse:
            self.max_pressure = max_press_array
            self.avg_pressure = avg_press_array
            self.min_pressure = min_press_array
            self.times_pressed = action_count_array
            if timelapse[0][1] is None:
                self.timelapse = 0 
            else:
                self.timelapse = timelapse[0][1]
            self.max_pressure = [0 if x is None else x for x in self.max_pressure]
            self.avg_pressure = [0 if x is None else x for x in self.avg_pressure]
            self.min_pressure = [0 if x is None else x for x in self.min_pressure]
            self.times_pressed = [0 if x is None else x for x in self.times_pressed]
        else:
            self.max_pressure = [0,0]
            self.avg_pressure = [0,0]
            self.times_pressed = [0,0]
            self.min_pressure = [0,0]
            self.timelapse = "00:00:00"
        self.min_chart.setOpts(height = self.min_pressure)
        self.avg_chart.setOpts(height = self.avg_pressure)
        self.max_chart.setOpts(height = self.max_pressure) 
        self.times_used_chart.setOpts(height = self.times_pressed)
        self.timelapseLabel.setText(self.timelapse)
        self.sessionNameLabel.setText(self.string_list_graphs[10].format(user = self.current_user_name))
        
    def button_toggler(self, clicked_button):
        for button in self.ui.buttonsContainer.findChildren(QPushButton):
            if button != clicked_button:
                button.setEnabled(True)
            else:
                clicked_button.setEnabled(False)
        self.sessionComboBox.setEnabled(not self.sessionComboBox.isEnabled())
        if self.startListening.isEnabled():
            self.newSessionButton.setDisabled(False)
            self.deleteSessionButton.setDisabled(False)
            self.exportSessionCSVButton.setDisabled(False)
            self.exportSessionImageButton.setDisabled(False)
            self.sideMenuDisableSignal.emit(True)
        else:
            self.newSessionButton.setDisabled(True)
            self.deleteSessionButton.setDisabled(True)
            self.exportSessionCSVButton.setDisabled(True)
            self.exportSessionImageButton.setDisabled(True)
            self.sideMenuDisableSignal.emit(False)                
            
    def get_sessions(self):
        qSessions = f"select * from session where patient_id = ?;"
        resSessions = self.dbHandleClass.execute_single_query(qSessions,[self.current_user])
        if resSessions:
            return resSessions
    
    def populate_comboBox(self):
        self.sessionComboBox.clear()
        sessions = self.get_sessions()
        if sessions:
            for s in sessions:
                text = str(s[2])
                latest_session = s[0]
                self.assing_latest_session(latest_session)
                self.sessionComboBox.addItem(text[:len(text)-3],s[0])
            self.sessionComboBox.setCurrentIndex(self.sessionComboBox.count()-1)
            
    def assing_latest_session(self,latest_session):
        print(f"assing_latest_session:{latest_session}")
        self.latest_session = latest_session
        self.dataCollectorHandler.current_session_index = latest_session

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
            self.delete_charts()
            self.create_charts()
            self.update_session_chart_value()
            self.update_summary_charts()
        return super().changeEvent(event)
        