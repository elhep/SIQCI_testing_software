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
    [0, 18.0, 3],
    [0, 18.0, 4],
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
]

class Pin():
    def __init__(self, type, number):
        self.default_v = type[number][0]
        self.max_v     = type[number][1]
        self.column  = type[number][2]
        if self.max == 1.8:
            self.bank    =  1
        elif self.max == 3.3:
            self.bank    =  2
        elif self.max == 18.0:
            self.bank    =  3
        elif self.max == 45.0:
            self.bank    =  4
        self.default_row = PWR if self.default ==  self.max else GND


# class Pins:
#     gates = [
#         [1.8,  1.8, 1],
#         [  0,  1.8, 2],
#         [3.3,  3.3, 1],
#         [  0,  3.3, 2],
#         [  0, 18.0, 1],
#         [  0, 18.0, 2],
#         [  0, 18.0, 3],
#         [  0, 18.0, 4],
#     ]
#     sources = [
#         [0, 1.8, 3],
#         [0, 1.8, 4],
#         [0, 1.8, 5],
#         [0, 1.8, 6],
#         [0, 3.3, 3],
#         [0, 3.3, 4],
#         [0, 3.3, 5],
#         [0, 3.3, 6],
#         [0, 45.0, 1],
#         [0, 45.0, 2],
#         [0, 45.0, 3],
#         [0, 45.0, 4],
#         [0, 45.0, 5],
#         [45.0, 45.0, 6],
#         [45.0, 45.0, 7],
#         [45.0, 45.0, 8],
#         [45.0, 45.0, 9],
#         [45.0, 45.0, 10],
#     ]
#     drains = [
#         [0, 1.8, 7],
#         [0, 1.8, 8],
#         [0, 1.8, 9],
#         [0, 1.8, 10],
#         [0, 3.3, 7],
#         [0, 3.3, 8],
#         [0, 3.3, 9],
#         [0, 3.3, 10],
#         [0, 45.0, 11],
#         [0, 45.0, 12],
#         [0, 45.0, 13],
#         [0, 45.0, 14],
#         [0, 45.0, 15],
#         [45.0, 45.0, 16],
#         [45.0, 45.0, 17],
#         [45.0, 45.0, 18],
#         [45.0, 45.0, 19],
#         [45.0, 45.0, 20],
#     ]
#
#     '''
#     Return max or default value of the pin
#     '''
#     @classmethod
#     def pin_value(cls, pin_type, pins, value_type):
#         if value_type == "max":
#             pos = 1
#         elif value_type == "default":
#             pos = 0
#         else:
#             print(value_type)
#             raise ValueError("value_type not supported")
#         if pin_type == "gate":
#             return cls.gates[pins[0]][pos]
#         elif pin_type == "source":
#             return cls.sources[pins[1]][pos]
#         elif pin_type == "drain":
#             return cls.drains[pins[2]][pos]
#         else:
#             print(pin_type)
#             raise ValueError("pin_type not supported")
#
#     '''
#     Return column number in 3732 card for the specific pin
#     '''
#     @classmethod
#     def column(cls, pin_type, pins):
#         if pin_type == "gate":
#             return cls.gates[pins[0]][3]
#         elif pin_type == "source":
#             return cls.sources[pins[1]][3]
#         elif pin_type == "drain":
#             return cls.drains[pins[2]][3]
#         else:
#             print(pin_type)
#             raise ValueError("pin_type not supported")

def cmos(dmm):
    for transistor in mos:
        t = MOS(transistor, dmm)
        t.perform_measurements()
    NotImplemented()

class MOS():
    def __init__(self, data, keithley_controller):
        self.name = data[0]
        self.volt = data[1]
        self.type = data[2]
        self.pins = data[3]
        self.gate = Pin(gates, data[3][0])
        if self.type == "n":  # source on SOURCE pin
            self.source = Pin(sources, data[3][1])
            self.drain  = Pin(drains, data[3][2])
        else:                 # source on DRAIN pin
            self.source = Pin(drains, data[3][1])
            self.drain  = Pin(sources, data[3][2])
        self.dmm_channel = data[4]
        self.dmm = keithley_controller
        self.switch_card = keithley_controller.cards[0]
        self.matrix_card = keithley_controller.cards[1]
        assert self.switch_card.__class__.__name__ == "Model_3723_2B"
        assert self.matrix_card.__class__.__name__ == "Model_3732_4B"

    def perform_measurements(self):
        self.prepare_relays()
        self.save_data(self.type+self.name+str(self.volt)+"_transfer",self.transfer_ch())
        self.save_data(self.type+self.name+str(self.volt)+"_output", self.output_ch())
        self.back_to_default()

    def save_data(self, file_name, gate_values, drain_values, data):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(gate_values)
            writer.writerow(drain_values)
            writer.writerows(data)

    '''
    Prepare relays at first setup (before turning on PSU)
    '''
    def setup(self):
        for pin in [self.gate, self.drain, self.source]:
            self.matrix_card.switch(bank=pin.bank, row=pin.default_row, column=pin.column)

    '''
    Connect gate and drain to proper VADJs
    '''
    def prepare_measurements(self, src_state, gate_v, drain_v):
        self.switch_card.switch(self.dmm_channel)
        # Set VADJ0 to default value of gate
        self.vsup("VADJ0", self.gate.default_v)

        # Set VADJ1 to default value of drain
        self.vsup("VADJ1", self.drain.default_v)

        # Switch gate from default value to vadj0
        # self.dmm.c3732.open(bank = self.gate.bank, row = self.gate.default_row, column = self.gate.column) #TODO check if it was open
        # self.dmm.c3732.close(bank = self.gate.bank, row = VADJ0, column = self.gate.column)         #TODO check if will not cross with something
        self.matrix_card.switch(bank=self.gate.bank, row=VADJ0, column=self.gate.column) # should close previous first

        # Switch drain from default value to vadj1
        # self.dmm.c3732.open(bank = self.drain.bank, row = self.drain.default_row, column = self.drain.column)
        # self.dmm.c3732.close(bank = self.drain.bank, row = VADJ0 if self.drain.bank == 4 else VADJ1, column = self.drain.column) #VADJ1 at bank 4 is on row 3 (NOT 4 like in banks 1-3)
        self.matrix_card.switch(bank = self.drain.bank, row = VADJ0 if self.drain.bank == 4 else VADJ1, column = self.drain.column)

        if src_state != self.source.default_v:
            # self.dmm.c3732.open(bank=self.source.bank, row=self.source.default_row, column=self.source.column)
            # self.dmm.c3732.close(bank=self.source.bank, row=GND if src_state == 0 else PWR,
            #                      column=self.source.column)
            self.matrix_card.switch(bank=self.source.bank, row=GND if src_state == 0 else PWR,
                                 column=self.source.column)

        self.vsup("VADJ0", gate_v)
        self.vsup("VADJ1", drain_v)

    '''
    Restore default setup of MOS relays
    '''
    def reset_relays(self, src_state):
        self.vsup(VADJ0, self.gate.default_v)
        self.vsup(VADJ1, self.drain.default_v)
        if src_state != self.source.default_v:
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

    def transfer_ch(self):
        if self.type == "n":
            gate_start = 0
            source_start = 0
            gate_limit = self.gate.max_v
            drain_start = 0
            drain_limit = self.drain.max_v
            if self.volt == 1.8:
                gate_step   = 0.05
                drain_step  = 0.1
            elif self.volt == 3.3:
                gate_step = 0.1
                drain_step = 0.2
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
                gate_step   = -0.05
                drain_step  = -0.1
            elif self.volt == 3.3:
                gate_step = -0.1
                drain_step = -0.2
            else:  # 45V
                gate_step = -1
                drain_step = -5

        gate_values = [round(i,2) for i in np.arange(gate_start, gate_limit+gate_step, gate_step)]
        drain_values = [round(i,2) for i in np.arange(drain_start, drain_limit+drain_step, drain_step)]

        self.prepare_measurements(source_start, gate_start, drain_start)

        # begin measurements
        # Outer loop over drain change
        # Inner loop over gate change
        data = list()
        for drain_vadj in drain_values:
            # change drain voltage
            self.vsup(VADJ1, drain_vadj)
            single_family = list()
            for gate_vadj in gate_values:
                self.vsup(VADJ0, gate_vadj)
                # measurements
                current = self.meas.get_voltage()/0.1   #0.1 R resistor
                single_family.append(current)  #TODO Do we want to set current limit?

                if current >= 0.04: # 40 mA limit
                    break
            data.append(single_family)

        #switch all pins to default voltage sources
        self.reset_relays(source_start)

        return {gate_values, drain_values, data}

    def output_ch(self):
        # We doesn't check source values - it was set during transfer_ch
        if self.type == "n":
            gate_start = 0
            source_start = 0
            gate_limit = self.gate.max_v
            drain_start = 0
            drain_limit = self.drain.max_v
            if self.volt == 1.8:
                gate_step   = 0.1
                drain_step  = 0.05
            elif self.volt == 3.3:
                gate_step = 0.2
                drain_step = 0.1
            else: # 45V
                gate_step = 3
                drain_step = 1
        else:
            gate_start   = self.gate.max_v
            gate_limit   = 0
            source_start = self.source.max_v
            drain_start  = self.drain.max_v
            drain_limit  = 0
            if self.volt == 1.8:
                gate_step   = -0.1
                drain_step  = -0.05
            elif self.volt == 3.3:
                gate_step = -0.2
                drain_step = -0.1
            else:  # 45V
                gate_step = -3
                drain_step = -1

        gate_values = [round(i,2) for i in np.arange(gate_start, gate_limit+gate_step, gate_step)]
        drain_values = [round(i,2) for i in np.arange(drain_start, drain_limit+drain_step, drain_step)]

        self.prepare_measurements(source_start, gate_start, drain_start)
        # begin measurements
        # Outer loop over gate change
        # Inner loop over drain change
        data = list()
        for gate_vadj in gate_values:
            # change drain voltage
            self.vsup(VADJ1, drain_vadj)
            single_family = list()
            for drain_vadj in drain_values:
                self.vsup(VADJ0, gate_vadj)
                # measurements
                current = self.meas.get_voltage()/0.1   #0.1 R resistor
                single_family.append(current)  #TODO Do we want to set current limit?

                if current >= 0.04: # 40 mA limit
                    break
            data.append(single_family)

        # switch all pins to default voltage sources
        self.reset_relays(source_start)

        return {gate_values, drain_values, data}