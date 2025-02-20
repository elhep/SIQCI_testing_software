import h5py
import matplotlib.pyplot as plt
import numpy as np
import csv
import os, glob

# print("dataset")
# print(f['__BV_Dataset__Data__'])
class PResults():
    def __init__(self, sd, sg, dv, dc, gv, gc):
        self.sweep_drain = sd
        self.sweep_gate  = sg
        self.drain_voltage = dv
        self.drain_current = dc
        self.gate_voltage = gv
        self.gate_current = gc
        
# DACs results
class DResults():
    def __init__(self, file, data):
        self.asic_id = file[4]
        self.id = file[-5]
        self.data = [float(value) for value in data]
        
    def __call__(self, *args, **kwds):
        return "ASIC{} DAC {}".format(self.asic_id, self.id)
    
    def __str__(self):
        return "ASIC{} DAC {}".format(self.asic_id, self.id)
            
        
    def draw(self):
        plt.figure()
        x_values = [i for i in range(0, 1024)]
        plt.plot(x_values, self.data)
        # x_values = list()
        # for _ in range(len(y_values)):
            # x_values.append(self.sweep_gate)
        # lines = plt.step(x_values, y_values)
        plt.xlabel("Digital code [LSB]")
        plt.ylabel("Output Voltage [V]")
        plt.title(self())
        plt.draw()
        
    def draw_diff(self, other):
        plt.figure()
        x_values = [i for i in range(0, 1024)]
        y_values = [x1 - x2 for x1, x2 in zip(self.data, other.data)]
        plt.plot(x_values, y_values)
        # x_values = list()
        # for _ in range(len(y_values)):
            # x_values.append(self.sweep_gate)
        # lines = plt.step(x_values, y_values)
        plt.xlabel("Digital code [LSB]")
        plt.ylabel("Output Voltage [V]")
        plt.title("DAC diff: ASIC {} DAC {} vs ASIC {} DAC {}".format(self.asic_id, self.id, other.asic_id, other.id))
        plt.draw()
        
        
class TResults():
    def __init__(self, file, sd, sg, dv, dc, gv, gc):
        self.block = file[12] # M for transistor from 1st block, X for transistor with MUX
        self.id   = int(file[13:15])
        if file[16:18] == 'MU':
            self.volt = 3.3
        else:
            self.volt = int(file[16:18])        
        self.type = file[19:23]
        self.asic_id = file[-5]
        self.sweep_drain = list(set(sd))
        self.sweep_drain.sort(reverse=False if self.type == "NMOS" else True)
        self.sweep_gate  = list(set(sg))
        self.sweep_gate.sort(reverse=False if self.type == "NMOS" else True)
        # we need to delete some values at the beginning of the file - we have to found first value in sweeps
        # which is not 0 V - then go back one step
        #first_index, last_index = self.find_first_last_index(sd, sg)
        drain_voltage = dv#[first_index:-last_index]
        drain_current = dc#[first_index:-last_index]
        gate_voltage = gv#[first_index:-last_index]
        gate_current = gc#[first_index:-last_index]
        sweep_drain = sd#[first_index:-last_index]
        sweep_gate =  sg#[first_index:-last_index]
        self.points = list()
        for meas_point in zip(sweep_drain,
                                  sweep_gate,
                                  drain_voltage,
                                  drain_current,
                                  gate_voltage,
                                  gate_current):
            self.points.append(PResults(*meas_point))
            
    def __sub__(self, other):
        results = list()
        for points_s in self.points:
            if points_s.sweep_gate == 0.0:
                continue
            if points_s.sweep_drain == 0.0:
                continue
            for point in other.points:
                if (point.sweep_gate == points_s.sweep_gate) and \
                    (point.sweep_drain == points_s.sweep_drain):
                        other_point = point
                        break
                else:
                    continue
            try:
                results.append([
                    True if abs(points_s.drain_voltage - other_point.drain_voltage)/points_s.drain_voltage >= 0.005 else False,
                    True if abs(points_s.drain_current - other_point.drain_current)/points_s.drain_current >= 0.005 else False,
                    True if abs(points_s.gate_voltage - other_point.gate_voltage)/points_s.gate_voltage >= 0.005 else False,
                    True if abs(points_s.gate_current - other_point.gate_current)/points_s.gate_current >= 0.005 else False,
                ])
            except:
                pass
            try:
                results[-1].index(True)
                results[-1].append(points_s.sweep_gate)
                results[-1].append(points_s.sweep_drain)
                results[-1].append(other_point.sweep_gate)
                results[-1].append(other_point.sweep_drain)
            except ValueError:
                pass
            
        return results
        
    def find_first_last_index(self, sd, sg):
        for id, values in enumerate(zip(sd, sg)):
            if (values[0] != 0) or (values[1] !=0):
                first = id-1
                break
        for id, values in enumerate(zip(reversed(sd), reversed(sg))):
            if (values[0] != 0) or (values[1] !=0):
                return first, id+1    
            
    def __call__(self, *args, **kwds):
        return "ASIC{} transistor {}{} {}".format(self.asic_id, self.block, self.id, self.type)
    
    def __str__(self):
        return "ASIC{} transistor {}{} {}".format(self.asic_id, self.block, self.id, self.type)
            
    def draw(self):
        plt.figure()
        x_values = self.sweep_gate
        y_values = list()
        for _ in range(len(self.sweep_drain)):
            y_values.append(list())
        for y in self.points:
            id = self.sweep_drain.index(y.sweep_drain)
            y_values[id].append(y.drain_current)
        for y in y_values:
            plt.plot(x_values, y)
        # x_values = list()
        # for _ in range(len(y_values)):
            # x_values.append(self.sweep_gate)
        # lines = plt.step(x_values, y_values)
        
        plt.legend(self.sweep_drain)
        plt.xlabel("Vgs [V]")
        plt.ylabel("Ids [A]")
        plt.title(self())
        plt.draw()
        
    def draw_out(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x_values = self.sweep_drain
        y_values = list()
        for _ in range(len(self.sweep_gate)):
            y_values.append(list())
        for y in self.points:
            id = self.sweep_gate.index(y.sweep_gate)
            y_values[id].append(y.drain_current)
        for y in y_values:
            ax.plot(x_values, y)
            
        ax.legend(self.sweep_gate)
        plt.xlabel("Vds [V]")
        plt.ylabel("Ids [A]")
        plt.title(self())
        from matplotlib.widgets import Cursor
        cursor = Cursor(ax, useblit=True)
        plt.draw()
        
class SIQCIPostProcessing():
    def __init__(self):
        self.gate_points_nb = 21
        self.drain_points_nb = 11
        self.transistors = list()
        self.dacs = list()
        
        files = glob.glob('*.csv')
        for t in files:
            self.transistors.append(self.import_keysight_data(t))
            
        files = glob.glob('*.txt')
        for t in files:
            self.transistors.append(self.import_transistor_data(t))
            
        files = glob.glob('*.dac')
        for t in files:
            self.dacs.append(self.import_dac_data(t))
            
    def list_of_transistors(self):
        for id, t in enumerate(self.transistors):
            print("{}: {}".format(id, t))
            
    def import_dac_data(self, file):
        with open(file) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar=" ")
            for row in enumerate(spamreader):
                return DResults(file, row[1])
                    
            
    def import_transistor_data(self, file):
        sweep_drain = list()
        sweep_gate = list()
        drain_voltage = list()
        drain_current = list()
        gate_voltage = list()
        gate_current = list()
        with open(file) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar=" ")
            for row in enumerate(spamreader):
                    row = row[1]
                    drain_voltage.append(float(row[2]))
                    drain_current.append(float(row[3]))
                    gate_voltage.append(float(row[0]))
                    gate_current.append(float(row[1]))
                    sweep_drain.append(float(row[5]))
                    sweep_gate.append(float(row[4]))
                    
        return TResults(file, sweep_drain, sweep_gate, drain_voltage, drain_current, gate_voltage, gate_current)
                
            
    def import_keysight_data(self, file):
        sweep_drain = list()
        sweep_gate = list()
        drain_voltage = list()
        drain_current = list()
        gate_voltage = list()
        gate_current = list()
        data_row = -1
        with open(file) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar="|")
            for idr,row in enumerate(spamreader):
                for idc, cell in enumerate(row):
                    if cell.find("Sweep DRAIN Voltage Setting") != -1:
                        sweep_drain_voltage_column_id = idc
                    if cell.find("Sweep GATE Voltage Setting") != -1:
                        sweep_gate_voltage_column_id = idc
                    if cell.find("Get GATE Voltage Measurement") != -1:
                        gate_voltage_column_id = idc
                    if cell.find("Get DRAIN Voltage Measurement") != -1:
                        drain_voltage_column_id = idc
                    elif cell.find("Get CH1 Voltage Measurement") != -1:
                        drain_voltage_column_id = idc
                    if cell.find("Get GATE Current Measurement") != -1:
                        gate_current_column_id = idc
                    if cell.find("Get DRAIN Current Measurement") != -1:
                        drain_current_column_id = idc
                        data_row = idr+1
                        break
                    elif cell.find("Get CH1 Current Measurement") != -1:
                        drain_current_column_id = idc
                        data_row = idr+1
                        break
                if idr == data_row:
                    break
            for idr,row in enumerate(spamreader):
                if idr < data_row:
                    continue
                if row[sweep_drain_voltage_column_id] == '' or \
                    row[sweep_gate_voltage_column_id] == '' or \
                    row[gate_voltage_column_id] == '' or \
                    row[gate_current_column_id] == '' or \
                    row[drain_current_column_id] == '' or \
                    row[drain_voltage_column_id] == '':
                        continue
                else:
                    sweep_drain.append(float(row[sweep_drain_voltage_column_id].replace(",", ".")))
                    sweep_gate.append(float(row[sweep_gate_voltage_column_id].replace(",", ".")))
                    drain_voltage.append(float(row[drain_voltage_column_id].replace(",", ".")))
                    drain_current.append(float(row[drain_current_column_id].replace(",", ".")))
                    gate_voltage.append(float(row[gate_voltage_column_id].replace(",", ".")))
                    gate_current.append(float(row[gate_current_column_id].replace(",", ".")))
                    
            return TResults(file, sweep_drain, sweep_gate, drain_voltage, drain_current, gate_voltage, gate_current)
        

x = SIQCIPostProcessing()
x.list_of_transistors()
for d in x.dacs:
    d.draw()
    x.dacs[0].draw_diff(d)
# for t in x.transistors:
    # t.draw()
    # t.draw_out()
# for point in (x.transistors[0]-x.transistors[1]):
    # print(point)

plt.show()

input("FINISH")

