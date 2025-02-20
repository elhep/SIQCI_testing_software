import socket
import csv
import time
from arduino_scripts.dac import SR

class WD():
    def __init__(self, smu0, smu1):
        self.counter = 0
        self.limit = 10
        self.smu0 = smu0
        self.smu1 = smu1
        
    def reset(self):
        self.counter = 0
        
    def tick(self, exit_id):
        self.counter += 1
        if self.counter == self.limit:
            self.smu1.set_output_state(False)
            self.smu0.set_output_state(False)
            print("Diode problem!!!")
            exit(exit_id)

# whole experiment for transistors
class SIQCI():
    def __init__(self):
        self.gate_points_nb = 21
        self.drain_points_nb = 11
        self.gate_smu = SMU('192.168.95.179')
        self.drain_smu = SMU('192.168.95.146')
        
    def run_test(self, bank, type, asic, transistors=None):
        if (bank != 1.8) and (bank != 3.3) and (bank != 45) and (bank != "MUX"):
            raise "Error: bank type not supported. Use: 1.8 / 3.3 / 45 / 'MUX'"
        if (type != "NMOS") and (type != "PMOS"):
            raise "Error: tranistor type not supported. Use 'NMOS' or 'PMOS'"
        self._reset_devices()
        self._common_prepare()
        self._prepare_specific_bank(type, bank if bank != "MUX" else 3.3)
        if bank == "MUX": 
            sr = SR()
            if transistors is None:
                for i in range(64):
                    sr.set_active_nmos(i)
                    self._perform_transistor_test(i, asic, type, "MU")
            else:
                for id in transistors:
                    sr.set_active_nmos(i)
                    self._perform_transistor_test(id, asic, type, "MU")
        elif transistors is None:
            for i in range(4):
                input("Prepare connection for measurements: Transistor:{} Type:{} Bank:{} \n Press enter to continue".format(i, type, bank))
                self._perform_transistor_test(i, asic, type, bank if bank.is_integer else int(bank*10))
        else:
            for id in transistors:
                input("Prepare connection for measurements: Transistor:{} Type:{} Bank:{} \n Press enter to continue".format(id, type, bank))
                self._perform_transistor_test(id, asic, type, bank if bank.is_integer else int(bank*10))
                
            

            
    def _reset_devices(self):
        self.gate_smu.reset()
        self.drain_smu.reset()
        try:
            self.gate_smu.socket.recv(300).decode('utf-8').strip()
        except:
            print("Done")
        try:
            self.drain_smu.socket.recv(300).decode('utf-8').strip()
        except:
            print("Done")
    
    def _common_prepare(self):
        # Output mode VOLT
        self.drain_smu.set_output_mode("VOLT")
        self.gate_smu.set_output_mode("VOLT") 
        # Overcurrent limits
        self.drain_smu.set_ocp_limit("0.01")
        self.gate_smu.set_ocp_limit("0.01")
        # Sweep mode
        self.gate_smu.write(":SOUR:VOLT:MODE SWE")
        self.drain_smu.write(":SOUR:VOLT:MODE LIST")
        # self.drain_smu.write(":SOUR:VOLT:POIN 12")
        # Sensing curr and volt
        self.gate_smu.write(':sens:func "curr","volt"')
        self.drain_smu.write(':sens:func "curr","volt"')
        # Low terminal floating
        self.gate_smu.write(':outp:low flo')
        self.drain_smu.write(':outp:low flo')
        #
        self.gate_smu.write(":SOUR:VOLT:STAR 0") #always 0, for NMOS and PMOS
        self.drain_smu.write(":SOUR:VOLT:STAR 0") 
        
        # Set init voltage
        self.drain_smu.set_voltage_settings(0)
        self.gate_smu.set_voltage_settings(0)
        

        # Triggers for gate + counter for trigger
        # Sets trigger count :TRIG[c]<:ACQ | :TRAN | [:ALL]>:COUN value
        self.gate_smu.write(":trig:coun {}".format(self.gate_points_nb))
        # [:SOUR[c]]:TOUT[:STAT] mode
        self.gate_smu.write(":TOUT 1") # action trigger is connected to OUTPUT
        self.gate_smu.write(":DIG:EXT1:FUNC TOUT") # EXT1 IO configure to output
        self.gate_smu.write(":trig:tim 0.5") # interval for gate sweep loop
        self.gate_smu.write(":trig:acq:del 0.001") # get gate measurements 1 ms after switching to new value
        
        # Triggers for drain + counter for trigger
        self.drain_smu.write(":arm:coun {}".format(self.gate_points_nb))
        self.drain_smu.write(":arm:sour EXT1")
        self.drain_smu.write(":trig:tran:coun {}".format(self.drain_points_nb+1))
        self.drain_smu.write(":trig:acq:coun {}".format(self.drain_points_nb))
        self.drain_smu.write(":trig:acq:del 0.0003")
        self.drain_smu.write(":trig:tim 0.0006") # interval for gate sweep loop
        self.drain_smu.write(":arm:del 0.02")
        self.drain_smu.write(":trig:sour tim")
        # 

    def _prepare_specific_bank(self, type, voltage):
        # Set voltage range
        self.drain_smu.set_voltage_range("21" if voltage >= 2.1 else "2.1") # TODO check if 2.1 works or should be 2,1
        self.gate_smu.set_voltage_range("21" if voltage >= 2.1 else "2.1") # TODO check if 2.1 works or should be 2,1

        # Configure sweep steps: GATE (21 points):
        self.gate_smu.write(":SOUR:VOLT:STOP {}".format(voltage if type == "NMOS" else -voltage))
        self.gate_smu.write(":SOUR:VOLT:STEP {}".format((voltage if type == "NMOS" else -voltage)/(self.gate_points_nb-1))) # sign always +: SMU will figure out that should substract value, not add 
        # self.drain_smu.write(":SOUR:VOLT:STOP {}".format(voltage if type == "NMOS" else -voltage))
        # self.drain_smu.write(":SOUR:VOLT:STEP {}".format(voltage/10)) # sign always +: SMU will figure out that should substract value, not add 
        drain_points = str()
        for x in range(0, int(voltage*1000)+1, int(voltage*1000/(self.drain_points_nb-1))):
            drain_points += str(x/1000) + "," if type == "NMOS" else str(-x/1000) + ","
        drain_points += "0.0"# if type == "NMOS" else str(voltage)
        self.drain_smu.write(":sour:list:volt {}".format(drain_points))
        
    def _perform_transistor_test(self, id, asic, type, bank):
        name="Przejsciowa_M{:02d}_{}_{}_ASIC{}".format(id, bank, type, asic)
        name = name.replace(".", "")
        # print(name)
        self.gate_smu.set_output_state(True)
        self.drain_smu.set_output_state(True)
        
        self.drain_smu.write(":init (@1)")
        self.gate_smu.write(":init (@1)")
        
        while self.gate_smu.ask(":idle?").find("1\r") != 8:
            time.sleep(1)
        #make sure that we have clear buffer
        time.sleep(3)
        try:
            self.gate_smu.socket.recv(50000).decode('utf-8').strip()
        except:
            pass
        try:
            self.drain_smu.socket.recv(50000).decode('utf-8').strip()
        except:
            pass
        
        
        x = self.gate_smu.ask(":fetc:arr:curr? (@1)")
        y = self.gate_smu.ask(":fetc:arr:volt? (@1)")
        x2 = self.drain_smu.ask(":fetc:arr:curr? (@1)")
        y2 = self.drain_smu.ask(":fetc:arr:volt? (@1)")
        
        # time.sleep(3)
        # while self.drain_smu.ask(":outp?").find("0\r") != 8:
        self.drain_smu.set_output_state(False)
        # while self.gate_smu.ask(":outp?").find("0\r") != 8:
        self.gate_smu.set_output_state(False)
        
        # print(x)
        # print(y)
        # print(x2)
        # print(y2)

        x = x[x.find(')')+3:-9]
        y = y[y.find(')')+3:-9]
        x2 = x2[x2.find(')')+3:-9]
        y2 = y2[y2.find(')')+3:-9]
        self._generate_csv(x,y,x2,y2, name, bank, type)

        # with open("test2.txt", 'w', newline='') as file:
            # file.writelines(x)
            # file.writelines(y)
            # file.writelines(x2)
            # file.writelines(y2)
            # print("File created")
        
    def _generate_csv(self, x, y, x2, y2, name, bank, type):
        gate_v = list()
        drain_v = list()
        gate_c = list()
        drain_c = list()
        if bank == 'MU':
            bank = 3.3
        step_g = round(bank/(self.gate_points_nb-1),3)
        step_d = round(bank/(self.drain_points_nb-1),3)
        if type == "NMOS":
            start=0
            stop = bank
        else:
            start=0
            stop = -bank
            step_g = -step_g
            step_d = -step_d
        
        sweep_gate = [i/1000 for i in range(int(start*1000), int(stop*1000)+(1 if type == "NMOS" else -1), int(step_g*1000))]
        sweep_drain = [i/1000 for i in range(int(start*1000), int(stop*1000)+(1 if type == "NMOS" else -1), int(step_d*1000))]
        
        def extract_floats(inp):
            out = list()
            while inp.find(',') != -1:
                out.append(float(inp[:inp.find(',')]))
                inp = inp[inp.find(',')+1:]
            out.append(float(inp))
            return out
        
        gate_c = extract_floats(x)
        gate_v = extract_floats(y)
        drain_c = extract_floats(x2)
        drain_v = extract_floats(y2)
        final_gate_c = list()
        final_gate_v = list()
        final_sweep_g = list()
        final_sweep_d = list()
        for c, v, sg in zip(gate_c, gate_v, sweep_gate):
            # final_sweep_d.append(sd)
            for _ in range(self.drain_points_nb):
                final_gate_c.append(c)
                final_gate_v.append(v)
                final_sweep_g.append(sg)
        for _ in range(self.gate_points_nb):
            final_sweep_d += sweep_drain
                
        with open(name+".txt", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(zip(final_gate_v, final_gate_c, drain_v, drain_c, final_sweep_g, final_sweep_d))
            print("File created")
        
        
        
class SMU():
    def __init__(self, ip, debug = False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, 5024))
        self.socket.settimeout(1)       
        self.debug = debug 
        print(self.socket.recv(64))
        print(self.socket.recv(64))
        # print(self.ask("*IDN?"))
        
    def write(self, cmd):
        self.socket.send('{}\r'.format(cmd).encode('utf-8'))
        time.sleep(1)
        meta = self.socket.recv(500000).decode('utf-8').strip()
        # print("META write: " + meta)
        return meta
        # print("FINISH META write")
        
    def ask(self, cmd):
        data = self.write(cmd)
        # data = data[data.find('\n')+1:]
        # data = data[:data.find('\r')]
        return data
    
    # def long_ask(self, cmd):
    #     self.socket.send('{}\r'.format(cmd).encode('utf-8'))
    #     time.sleep(3)
    #     return self.socket.recv(5000).decode('utf-8').strip()

    
    def set_ocp_limit(self, value):
        self.write(":SENS:CURR:PROT {}".format(value)) # 
        
    def set_voltage_settings(self, value):
        self.write(":VOLT {}".format(value)) # if error: :SOUR:VOLT....
        
    def set_voltage_range(self, value):
        self.write(":SOUR:VOLT:RANG {}".format(value)) # 

        
    def set_output_state(self, state):
        if state:
            self.write(":OUTP 1")
        else:
            self.write(":OUTP 0")
            
    def set_output_mode(self, mode):
        self.write(":SOUR:FUNC:MODE {}".format(mode))
            
    def reset(self):
        self.write("*RST")
        self.write(':SENS:FUNC:ALL')
        
    def get_voltage(self):
        result = self.ask(":MEAS:VOLT?")
        # if self.debug:
        #     print(result)
        # data = self.socket.recv(300).decode('utf-8').strip()
        while True:
            try:
                return float(result)
            except:
                result = self.socket.recv(300).decode('utf-8').strip()
                result = result[result.find('\n')+1:]
                result = result[:result.find('\r')]
                
    def get_current(self):
        # self.write(":SENS:FUNC CURR")
        result = self.ask(":MEAS:CURR?")
        if self.debug:
            print(result)
        while True:
            try:
                return float(result)
            except:
                result = self.socket.recv(300).decode('utf-8').strip()
                result = result[result.find('\n')+1:]
                result = result[:result.find('\r')]
                

class PResults():
    def __init__(self, gv, dv, gc, dc):
        self.results = (gv, gc, dv, dc)
        
    def __str__(self):
        return self.results

class TResults():
    def __init__(self):
        self.results = list()
        
    def add(self, gv, dv, gc, dc):
        self.results.append([gv, dv, gc, dc])
        
        
    def export_to_csv(self, name):
        with open(name+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.results)
            print("File created")