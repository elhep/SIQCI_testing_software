import csv
import numpy as np

'''
List of all transistors in first measurements block.
    array[0] - transistor's name: str M*
    array[2] - subblock (voltage bank): float 1.8/3.3/45.0
    array[3] - type NMOS/CMOS: str n/p
    array[4] - number of pins: array(int gate, int source, int drain)
    array[5] - measurement channel (at 3723 card to DMM)
'''
mos = [
    # NMOS P1V8
    ["M0", 1.8, "n", [1, 0, 0], 1],
    ["M1", 1.8, "n", [1, 1, 1], 2],
    ["M2", 1.8, "n", [1, 2, 2], 3],
    ["M3", 1.8, "n", [1, 3, 3], 4],
    # PMOS P1V8
    ["M4", 1.8, "p", [0, 0, 0], 1],
    ["M5", 1.8, "p", [0, 1, 1], 2],
    ["M6", 1.8, "p", [0, 2, 2], 3],
    ["M7", 1.8, "p", [0, 3, 3], 4],
    # NMOS P3V3
    ["M0", 3.3, "n", [3, 4, 4], 5],
    ["M1", 3.3, "n", [3, 5, 5], 6],
    ["M2", 3.3, "n", [3, 6, 6], 7],
    ["M3", 3.3, "n", [3, 7, 7], 8],
    # PMOS P3V3
    ["M4", 3.3, "p", [2, 4, 4], 5],
    ["M5", 3.3, "p", [2, 5, 5], 6],
    ["M6", 3.3, "p", [2, 6, 6], 7],
    ["M7", 3.3, "p", [2, 7, 7], 8],
    # NMOS P45V0
    ["M0", 45.0, "n", [4, 8, 8], 9],
    ["M1", 45.0, "n", [4, 9, 9], 10],
    ["M2", 45.0, "n", [4, 10, 10], 11],
    ["M3", 45.0, "n", [4, 11, 11], 12],
    ["M4", 45.0, "n", [4, 12, 12], 13],
    ["M5", 45.0, "n", [5, 8, 8], 9],
    ["M6", 45.0, "n", [5, 9, 9], 10],
    ["M7", 45.0, "n", [5, 10, 10], 11],
    ["M8", 45.0, "n", [5, 11, 11], 12],
    ["M9", 45.0, "n", [5, 12, 12], 13],
    # PMOS P45V0
    ["M10", 45.0, "p", [6, 13, 13], 14],
    ["M11", 45.0, "p", [6, 14, 14], 15],
    ["M12", 45.0, "p", [6, 15, 15], 16],
    ["M13", 45.0, "p", [6, 16, 16], 17],
    ["M14", 45.0, "p", [6, 17, 17], 18],
    ["M15", 45.0, "p", [7, 13, 13], 14],
    ["M16", 45.0, "p", [7, 14, 14], 15],
    ["M17", 45.0, "p", [7, 15, 15], 16],
    ["M18", 45.0, "p", [7, 16, 16], 17],
    ["M19", 45.0, "p", [7, 17, 17], 18],
]

nmos = ["NMOS M0", 3.3, 'n', [8,None,18], 19]

'''
Number of rows in 3732 card
'''
GND = 1
PWR = 2
VADJ0 = 3
VADJ1 = 4

'''
List of all pins parameters for mos transistors.
array(float default voltage, float max voltage, int column in 3732 card bank)
'''
DEFAULT = 0
MAX = 1
COLUMN = 2
gates = [
    [1.8, 1.8, 1],
    [0, 1.8, 2],
    [3.3, 3.3, 1],
    [0, 3.3, 2],
    [0, 18.0, 1],
    [0, 18.0, 2],
    [18.0, 18.0, 3],
    [18.0, 18.0, 4],
    [0, 3.3, 11]
]
sources = [
    [0, 1.8, 3],
    [0, 1.8, 4],
    [0, 1.8, 5],
    [0, 1.8, 6],
    [0, 3.3, 3],
    [0, 3.3, 4],
    [0, 3.3, 5],
    [0, 3.3, 6],
    [0, 45.0, 1],
    [0, 45.0, 2],
    [0, 45.0, 3],
    [0, 45.0, 4],
    [0, 45.0, 5],
    [45.0, 45.0, 6],
    [45.0, 45.0, 7],
    [45.0, 45.0, 8],
    [45.0, 45.0, 9],
    [45.0, 45.0, 10],
]
drains = [
    [0, 1.8, 7],
    [0, 1.8, 8],
    [0, 1.8, 9],
    [0, 1.8, 10],
    [0, 3.3, 7],
    [0, 3.3, 8],
    [0, 3.3, 9],
    [0, 3.3, 10],
    [0, 45.0, 11],
    [0, 45.0, 12],
    [0, 45.0, 13],
    [0, 45.0, 14],
    [0, 45.0, 15],
    [45.0, 45.0, 16],
    [45.0, 45.0, 17],
    [45.0, 45.0, 18],
    [45.0, 45.0, 19],
    [45.0, 45.0, 20],
    [0, 3.3, 12]
]

class Pin():
    def __init__(self, type, number):
        self.default_v = type[number][0]
        self.max_v     = type[number][1]
        self.column  = type[number][2]
        if self.max_v == 1.8:
            self.bank    =  1
        elif self.max_v == 3.3:
            self.bank    =  2
        elif self.max_v == 18.0:
            self.bank    =  3
        elif self.max_v == 45.0:
            self.bank    =  4
        self.default_row = PWR if self.default_v ==  self.max_v else GND


class NMOSMeas():
    def __init__(self, pwr, dmm, vsup, arduino, perform, *args):
        self.dmm = dmm
        self.vsup = vsup
        self.perform = perform
        self.arduino = arduino
        self.t = MOS(nmos, self.dmm, self.vsup, pwr)
        self.t.setup()

    def setup(self):
        self.t.setup()

    def meas(self):
        if not self.perform:
            return 0
        else:
            self.arduino.switch_to_vadj()
            self.t.prepare_measurements(*self.t.transfer_start_parameters())
            self.t.pwr.switch_all_v(True)
            for i in range(64):
                self.t.name = "NMOS M{}".format(i)
                self.t.full_name = "NMOS MATRIX: M{}".format(i)
                self.arduino.set_nmos_channel(n=i)
                self.t.perform_measurements()
            self.t.reset_relays(self.t.output_source_parameter())


class CMOSMeas():
    def __init__(self, pwr, dmm, vsup, arduino, perform, *args):
        self.dmm = dmm
        self.vsup = vsup
        self.perform = perform
        self.arduino = arduino
        self.t = [MOS(transistor, self.dmm, self.vsup, pwr) for transistor in mos]
        for t in self.t:
            t.setup()


    def setup(self):
        for t in self.t:
            t.setup()

    def meas(self):
        if not self.perform:
            return 0
        else:
            self.arduino.switch_to_vadj()
            for t in self.t:
                t.prepare_measurements(*t.transfer_start_parameters())
                t.pwr.switch_all_v(True)
                t.perform_measurements()
                t.reset_relays(t.output_source_parameter())

class MOS():
    def __init__(self, data, keithley_controller, power_supply, pwr):
        self.name = data[0]
        self.volt = data[1]
        self.type = data[2]
        self.pins = data[3]
        self.gate = Pin(gates, data[3][0])
        self.pwr = pwr

        self.full_name = "Bank {} {} {}".format(self.volt, "NMOS" if self.type=="n" else "PMOS", self.name)
        if self.type == "n":  # source on SOURCE pin
            if data[3][1] is not None:
                self.source = Pin(sources, data[3][1])
            else:
                self.source = None
            self.drain  = Pin(drains, data[3][2])
        else:                 # source on DRAIN pin
            if data[3][1] is not None:
                self.source = Pin(drains, data[3][1])
            else:
                self.source = None
            self.drain  = Pin(sources, data[3][2])
        self.dmm_channel = data[4]

        self.dmm = keithley_controller
        self.switch_card = keithley_controller.cards[1]
        self.matrix_card = keithley_controller.cards[2]
        assert self.switch_card.__class__.__name__ == "Model_3723_2B"
        assert self.matrix_card.__class__.__name__ == "Model_3732_4B"

        self.vsup = power_supply

    def perform_measurements(self):
        print("\n :::::::::::::::::::::::::::::::::::::::::::::: ")
        print(" ::::Starting measurements for {}".format(self.full_name))
        print(" :::::::::::::::::::::::::::::::::::::::::::::: \n\n")
        # self.setup()#self.prepare_relays() #setup was done at startup function 
        gate_values, drain_values, data = self.transfer_ch()
        self.save_data(self.full_name +" transfer", gate_values, drain_values, data)
        gate_values, drain_values, data = self.output_ch()
        self.save_data(self.full_name +" output", gate_values, drain_values, data)
        #back to default state:
        # self.setup() #done by reset()
        self.switch_card.open_bank1() #disconnect vadj from matrix card (just in case)

    def save_data(self, file_name, gate_values, drain_values, data):
        print("\n ::::Saving data for {}\n".format(self.full_name))
        with open("results/"+file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(gate_values)
            writer.writerow(drain_values)
            writer.writerows(data)

    '''
    Prepare relays at first setup (before turning on PSU)
    '''
    def setup(self):
        print("\n ::::Setup: {}\n".format(self.full_name))
        for pin in [self.gate, self.drain, self.source if self.source is not None else self.gate, self.drain]:
            self.matrix_card.switch(bank=pin.bank, row=pin.default_row, column=pin.column)
    '''
    Connect gate and drain to proper VADJs
    '''
    def prepare_measurements(self, src_state, gate_v, drain_v):
        print("\n ::::Prepering measurements {}\n".format(self.full_name))
        self.switch_card.switch_channel(self.dmm_channel)
        # Set VADJ1 to default value of gate
        self.vsup.set_vamplitude("VADJ1", self.gate.default_v)

        # Set VADJ0 to default value of drain
        self.vsup.set_vamplitude("VADJ0", self.drain.default_v)

        # Connect VADJs (at 3723) to proper bank of 3732
        if self.gate.bank == 1: #bank 1 for 1.8V
            self.switch_card.switch_channel(60)
        elif self.gate.bank == 2: #bank 2 for 3.3V
            self.switch_card.switch_channel(59)
        else: # gate bank3, src/drain bank 4
            self.switch_card.switch_channel(58)

        # Switch gate from default value to vadj0
        # self.dmm.c3732.open(bank = self.gate.bank, row = self.gate.default_row, column = self.gate.column) #TODO check if it was open
        # self.dmm.c3732.close(bank = self.gate.bank, row = VADJ0, column = self.gate.column)         #TODO check if will not cross with something
        self.matrix_card.switch(bank=self.gate.bank, row = VADJ0 if self.gate.bank == 3 else VADJ1, column=self.gate.column) # should close previous first

        # Switch drain from default value to vadj1
        # self.dmm.c3732.open(bank = self.drain.bank, row = self.drain.default_row, column = self.drain.column)
        # self.dmm.c3732.close(bank = self.drain.bank, row = VADJ0 if self.drain.bank == 4 else VADJ1, column = self.drain.column) #VADJ1 at bank 4 is on row 3 (NOT 4 like in banks 1-3)
        self.matrix_card.switch(bank = self.drain.bank, row = VADJ0, column = self.drain.column)

        if self.source is not None:
            if src_state != self.source.default_v:
                # self.dmm.c3732.open(bank=self.source.bank, row=self.source.default_row, column=self.source.column)
                # self.dmm.c3732.close(bank=self.source.bank, row=GND if src_state == 0 else PWR,
                #                      column=self.source.column)
                self.matrix_card.switch(bank=self.source.bank, row=GND if src_state == 0 else PWR,
                                     column=self.source.column)

        self.vsup.set_vamplitude("VADJ1", gate_v)
        self.vsup.set_vamplitude("VADJ0", drain_v)

    '''
    Restore default setup of MOS relays
    '''
    def reset_relays(self, src_state):
        print("\n ::::Reseting relays {}\n".format(self.full_name))
        self.vsup.set_vamplitude("VADJ1", self.gate.default_v)
        self.vsup.set_vamplitude("VADJ0", self.drain.default_v)
        # if self.source is not None:
        #     if src_state != self.source.default_v:
                # self.dmm.c3732.open(bank=self.source.bank, row=GND if src_state == 0 else PWR,
                #                      column=self.source.column)
                # self.dmm.c3732.close(bank=self.source.bank, row=self.source.default_row, column=self.source.column)
        self.matrix_card.switch(bank=self.source.bank, row=self.source.default_row, column=self.source.column)


        # self.dmm.c3732.open(bank = self.gate.bank, row = VADJ0, column = self.gate.column)
        # self.dmm.c3732.close(bank = self.gate.bank, row = self.gate.default_row, column = self.gate.column)
        self.matrix_card.switch(bank = self.gate.bank, row = self.gate.default_row, column = self.gate.column)

        # Switch drain from default value to vadj1
        # self.dmm.c3732.open(bank = self.drain.bank, row = VADJ0 if self.drain.bank == 4 else VADJ1, column = self.drain.column) #VADJ1 at bank 4 is on row 3 (NOT 4 like in banks 1-3)
        # self.dmm.c3732.close(bank = self.drain.bank, row = self.drain.default_row, column = self.drain.column)
        self.matrix_card.switch(bank = self.drain.bank, row = self.drain.default_row, column = self.drain.column)
        self.switch_card.open(self.dmm_channel)

    def transfer_start_parameters(self):
        if self.type == "n":
            gate_start = 0
            source_start = 0
            gate_limit = self.gate.max_v
            drain_start = 0
            drain_limit = self.drain.max_v
            if self.volt == 1.8:
                gate_step   = 0.3#0.05 TODO return value
                drain_step  = 0.9#0.1
            elif self.volt == 3.3:
                gate_step = 0.3#0.1
                drain_step = 0.3#0.2
            else: # 45V
                gate_step = 1
                drain_step = 5
        else:
            gate_start   = self.gate.max_v
            source_start = self.source.max_v
            gate_limit   = 0
            drain_start  = self.drain.max_v
            drain_limit  = 0
            if self.volt == 1.8:
                gate_step   = -0.3#-0.05
                drain_step  = -0.9#-0.1
            elif self.volt == 3.3:
                gate_step = -0.3#-0.1
                drain_step = -0.3#-0.2
            else:  # 45V
                gate_step = -1
                drain_step = -5
        return source_start, gate_start, drain_start
    
    def output_source_parameter(self):
        if self.type == "n":
            source_start = 0
        else:
            source_start = self.source.max_v

        return source_start

    def transfer_ch(self):
        print("\n ::::Transfer {}\n".format(self.full_name))
        if self.type == "n":
            gate_start = 0
            source_start = 0
            gate_limit = self.gate.max_v
            drain_start = 0
            drain_limit = self.drain.max_v
            if self.volt == 1.8:
                gate_step   = 0.9#0.05
                drain_step  = 0.9#0.1
            elif self.volt == 3.3:
                gate_step = 1.65#0.1
                drain_step = 1.65#0.2
            else: # 45V
                gate_step = 6#1
                drain_step = 5
        else:
            gate_start   = self.gate.max_v
            source_start = self.source.max_v
            gate_limit   = 0
            drain_start  = self.drain.max_v
            drain_limit  = 0
            if self.volt == 1.8:
                gate_step   = -0.9#-0.05
                drain_step  = -0.9#-0.1
            elif self.volt == 3.3:
                gate_step = -1.65#-0.1
                drain_step = -1.65#-0.2
            else:  # 45V
                gate_step = -6#-1
                drain_step = -5

        gate_values = [round(i,2) for i in np.arange(gate_start, gate_limit+gate_step, gate_step)]
        if gate_values[-1] > gate_limit:
            print("Gate: {}".format(gate_values[-1]))
            gate_values.pop()
        elif gate_values[-1] < 0:
            print("Gate: {}".format(gate_values[-1]))
            gate_values.pop()
        drain_values = [round(i,2) for i in np.arange(drain_start, drain_limit+drain_step, drain_step)]
        if drain_values[-1] > drain_limit:
            print("Drain: {}".format(drain_values[-1]))
            drain_values.pop()
        elif drain_values[-1] < 0:
            print("Drain: {}".format(drain_values[-1]))
            drain_values.pop()

        # self.prepare_measurements(source_start, gate_start, drain_start)
        # self.switch_all_v(True)

        # begin measurements
        # Outer loop over drain change
        # Inner loop over gate change
        data = list()
        for drain_vadj in drain_values: #TODO implement function for scaning over parameters
            # change drain voltage
            self.vsup.set_vamplitude("VADJ0", drain_vadj)
            single_family = list()
            for gate_vadj in gate_values:
                self.vsup.set_vamplitude("VADJ1", gate_vadj)
                # measurements
                print("Current meas")
                # current = 0.01#self.meas.get_voltage()/0.1   #0.1 R resistor #TODO implement
                current = float(self.switch_card.meas_dcvolts(self.dmm_channel))
                print(current)
                single_family.append(current)  #TODO Do we want to set current limit?

                if current >= 0.04: # 40 mA limit
                    break
            self.vsup.set_vamplitude("VADJ1", gate_values[0]) #return to init value for safe VADJ1 switch
            data.append(single_family)
        self.vsup.set_vamplitude("VADJ0", drain_values[0]) #return to init value for safe VADJ0 switch
        #switch all pins to default voltage sources
        # self.reset_relays(source_start)

        return gate_values, drain_values, data

    def output_ch(self):
        print("\n ::::Output {}\n".format(self.full_name))
        # We doesn't check source values - it was set during transfer_ch
        if self.type == "n":
            gate_start = 0
            source_start = 0
            gate_limit = self.gate.max_v
            drain_start = 0
            drain_limit = self.drain.max_v
            if self.volt == 1.8:
                gate_step   = 0.9#0.1
                drain_step  = 0.9#0.05
            elif self.volt == 3.3:
                gate_step = 1.65#0.2
                drain_step = 1.65#0.1
            else: # 45V
                gate_step = 6#3
                drain_step = 5#1
        else:
            gate_start   = self.gate.max_v
            gate_limit   = 0
            source_start = self.source.max_v
            drain_start  = self.drain.max_v
            drain_limit  = 0
            if self.volt == 1.8:
                gate_step   = -0.9#-0.1
                drain_step  = -0.9#-0.05
            elif self.volt == 3.3:
                gate_step = -1.65#-0.2
                drain_step = -1.65#-0.1
            else:  # 45V
                gate_step = -6#-3
                drain_step = -5#-1

        gate_values = [round(i,2) for i in np.arange(gate_start, gate_limit+gate_step, gate_step)]
        if gate_values[-1] > gate_limit:
            print("Gate: {}".format(gate_values[-1]))
            gate_values.pop()
        elif gate_values[-1] < 0:
            print("Gate: {}".format(gate_values[-1]))
            gate_values.pop()
        drain_values = [round(i,2) for i in np.arange(drain_start, drain_limit+drain_step, drain_step)]
        if drain_values[-1] > drain_limit:
            print("Drain: {}".format(drain_values[-1]))
            drain_values.pop()
        elif drain_values[-1] < 0:
            print("Drain: {}".format(drain_values[-1]))
            drain_values.pop()

        # self.prepare_measurements(source_start, gate_start, drain_start)
        # begin measurements
        # Outer loop over gate change
        # Inner loop over drain change
        data = list()
        for gate_vadj in gate_values:
            # change drain voltage
            self.vsup.set_vamplitude("VADJ1", gate_vadj)
            single_family = list()
            for drain_vadj in drain_values:
                self.vsup.set_vamplitude("VADJ0", drain_vadj)
                # measurements
                print("Current meas")
                # current = 0.001 #self.meas.get_voltage()/0.1   #0.1 R resistor #TODO implement
                current = float(self.switch_card.meas_dcvolts(self.dmm_channel))
                print(current)
                single_family.append(current)  #TODO Do we want to set current limit?

                if current >= 0.04: # 40 mA limit
                    break
            self.vsup.set_vamplitude("VADJ0", drain_values[0]) #return to init value for safe VADJ0 switch
            data.append(single_family)
        self.vsup.set_vamplitude("VADJ1", gate_values[0]) #return to init value for safe VADJ1 switch
        # switch all pins to default voltage sources
        # self.reset_relays(source_start)

        return gate_values, drain_values, data