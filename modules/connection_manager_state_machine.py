from modules.log_class import logger

from PySide6.QtStateMachine import QState
from PySide6.QtCore import Signal

class IdleState(QState):
    def __init__(self, machine, bluetoothHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoothHandle
        self.functions = functions
        
    def onEntry(self, event):
        logger.debug("IdleState onEntry")
        self.functions["release_screen"]()
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("IdleState onExit")
        self.functions["disable_screen"](pairControl=False)
        return super().onExit(event)

#has to deal with 3 diferrent cases:
    #full pair a new device
    #full unpair a paired device
    #unpair a device connected device and pair a new device
class DisconnectionState(QState):

    disc_finish = Signal()
    conn_start = Signal()

    def __init__(self, machine, bluetoothHandle, btSerialHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoothHandle
        self.btSerialHandle = btSerialHandle
        self.functions = functions
        self.sp_case = None
        self.spp_counter = 0
        self.hid_counter = 0

    def onEntry(self, event):
        logger.debug("DisconnectionState onEntry")
        self.btHandle.spp_finish.connect(self.handle_finish)
        self.btHandle.hid_finish.connect(self.handle_finish)

        res = self.case_evaluation()
        logger.debug(f"DisconncetionState onEntry res:{res}")
        match(res):
            case 0:
                logger.debug(f"DisconnectionState case 0")
                self.btHandle.hid_device_unpair(self.btHandle.paired_device.device())
                self.btHandle.unpair_device(self.btHandle.paired_device.device().address().toString().lower())
                self.btSerialHandle.clear_socket() 
            case 1:
                logger.debug(f"DisconnectionState case 1")
                self.btHandle.hid_device_unpair(self.machine.selected_device[0])
                self.btHandle.unpair_device(self.machine.selected_device[0].address().toString().lower())   
            case 2:
                logger.debug(f"DisconnectionState case 2")
                self.sp_case = True
                self.btHandle.hid_device_unpair(self.btHandle.paired_device.device())
                self.btHandle.unpair_device(self.btHandle.paired_device.device().address().toString().lower())
                self.btHandle.hid_device_unpair(self.machine.selected_device[0])
                self.btHandle.unpair_device(self.machine.selected_device[0].address().toString().lower())  
                self.btSerialHandle.clear_socket() 

        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("DisconnectionState onExit")
        self.machine.full_pair = None
        self.sp_case = None
        self.spp_counter = 0
        self.hid_counter = 0
        return super().onExit(event)
    
    def handle_finish(self, status):
        if self.sp_case == True:
            res = self.sp_case_async_check(status)
        else:
            res = self.machine.async_check(status)
        logger.debug(f"DisconnectionState handle_finish res:{res}")
        if res == "disc_finish":
            logger.debug(f"DisconnectionState handle_finish disc_finish")
            self.conn_check()
        elif res == "conn_start":
            logger.debug(f"DisconnectionState handle_finish conn_start")
            self.btHandle.spp_finish.disconnect(self.handle_finish)
            self.btHandle.hid_finish.disconnect(self.handle_finish)
            self.conn_start.emit()
            
    def sp_case_async_check(self, status):
        if status == "hid":
            self.hid_counter += 1
        elif status == "spp":
            self.spp_counter += 1
        if self.spp_counter == 2 and self.hid_counter == 2:
            return "conn_start"

    def case_evaluation(self):
        #full unpair case
        if self.machine.selected_device[0] == None and self.btHandle.paired_device:
            return 0
        #full pair case
        elif self.machine.selected_device[0] and self.btHandle.paired_device == None:
            return 1
        #connected device and full pair case
        elif self.machine.selected_device[0] and self.btHandle.paired_device:
            return 2

    def conn_check(self):
        def finish_send(status):
            logger.debug(f"DisconnectionState conn_check")
            self.btHandle.hid_finish.disconnect(finish_send)
            self.disc_finish.emit()
        
        self.btHandle.hid_finish.disconnect(self.handle_finish)
        self.btHandle.spp_finish.disconnect(self.handle_finish)
        self.btHandle.hid_finish.connect(finish_send)
        self.btHandle.check_device_connection(self.machine.selected_device[0])
    
class ErrorState(QState):
    def __init__(self, machine, bluetoohHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.functions = functions
        
    def onEntry(self, event):
        logger.debug(f"ErrorState onEntry")
        self.functions["handle_process_ending_error"]("Erro no processo de conexão")
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug(f"ErrorState onExit")
        return super().onExit(event)

class ConnectionState(QState):
    
    conn_finish = Signal()
    
    def __init__(self, machine, bluetoohHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.functions = functions
        
    def onEntry(self, event):
        logger.debug("ConnectionState onEntry")
        self.btHandle.spp_finish.connect(self.handle_finish)
        self.btHandle.hid_finish.connect(self.handle_finish)
        if self.machine.selected_device:
            self.btHandle.hid_device_pair(self.machine.selected_device[0])
            # self.btHandle.pair_device(self.machine.selected_device[1].serviceUuid().toString(),self.machine.selected_device[0].address().toString())
            # self.btHandle.create_service_socket(self.machine.selected_device[1])
            self.btHandle.spp_finish.emit("spp")
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("ConnectionState onExit")
        self.btHandle.spp_finish.disconnect(self.handle_finish)
        self.btHandle.hid_finish.disconnect(self.handle_finish)
        return super().onExit(event)

    def handle_finish(self, status):
        res = self.machine.async_check(status)

        if res == "conn_finish":
            self.conn_finish.emit()

class DeviceSearchState(QState):
    
    search_end = Signal()
    
    def __init__(self, machine, bluetoohHandle, funtions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.functions = funtions
        self.device_counter = 0

    def onEntry(self, event):
        logger.debug("DeviceSearchState onEntry")
        self.device_counter = 0
        self.machine.search = True
        self.btHandle.spp_finish.connect(self.handle_finish)
        self.btHandle.hid_finish.connect(self.handle_finish)
        self.btHandle.le_finish.connect(self.handle_power_finish)
        self.btHandle.hid_device_discovery()
        self.btHandle.spp_service_discovery()
        return super().onEntry(event)

    def onExit(self, event):
        logger.debug("DeviceSearchState onExit")
        self.btHandle.spp_finish.disconnect(self.handle_finish)
        self.btHandle.hid_finish.disconnect(self.handle_finish)
        self.btHandle.le_finish.disconnect(self.handle_power_finish)
        self.machine.search = None
        return super().onExit(event)

    def handle_finish(self, status):
        res = self.machine.async_check(status)

        if res == "search_end":
           self.device_power_check()

    def device_power_check(self):
        self.device_counter = len(self.btHandle.hid_device_list)
        logger.debug(f"DeviceSearchState device_power_check self.device_counter:{self.device_counter}")
        if self.device_counter > 0:
            for device in self.btHandle.hid_device_list:
                self.btHandle.low_energy_check(device)
    
    def handle_power_finish(self, res):
        logger.debug(f"DeviceSearchState handle_power_finish res:{res}")
        if res:
            self.device_counter -= 1
            self.btHandle.unpowered_device_list.append(res)
        else:
            self.device_counter -= 1

        if self.device_counter == 0:
            for controller in self.btHandle.le_controller_list:
                self.clear_le_controller(controller)
            
    def clear_le_controller(self,controller):
        def on_disc():
            controller.deleteLater()
            self.btHandle.le_controller_list.pop(self.btHandle.le_controller_list.index(controller))
            if len(self.btHandle.le_controller_list) == 0:
                self.search_end.emit()

        controller.disconnected.connect(on_disc)
        controller.disconnectFromDevice()

class FindPortState(QState):

    pair_success = Signal(str)

    def __init__(self, machine, bluetoohHandle, btSerialHandle, functions = None):
        super().__init__(machine)
        self.machine = machine
        self.btHandle = bluetoohHandle
        self.btSerialHandle = btSerialHandle
        self.functions = functions

    def onEntry(self, event):
        if self.machine.addr:
            self.btSerialHandle.port_finish.connect(self.on_socket_sucess)
            self.btSerialHandle.create_service_socket(self.machine.selected_device[1])
        return super().onEntry(event)

    def onExit(self, event):
        self.btHandle.paired_device = self.machine.selected_device[1]
        self.machine.selected_device = [None, None]
        self.machine.addr = None
        self.btSerialHandle.port_finish.disconnect(self.on_socket_sucess)
        return super().onExit(event)

    def on_socket_sucess(self):
        self.pair_success.emit(self.machine.addr)