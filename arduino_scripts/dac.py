import serial
import time
import socket
import csv


    
class SR():
    def __init__(self):
        i = 0
        while True:
            try:
                ser = serial.Serial(
                    port = "COM" + str(i),
                    baudrate=9600,
                )
                break
            except:
                i += 1
        self.reg = 0
        self.ser = ser
        self.ser.write(bytes([0xab, 0x03])) # calibration
        print(self.ser.read_until())
        print(self.ser.read_until())
        print(self.ser.read_until())
        print(self.ser.read_until())
        
    def update_asic(self):
        data = [0]*4
        for i in range(4):
            data[i] = ((self.reg >> (8*(3-i))) & 0xFF)
        # print(self.reg)
        # print(data)
        # print([0xab, 0x01] + data)
        self.ser.write(bytes([0xab, 0x01]+data))
        print(self.ser.read_until()) # single line to confirm new value
        
    def active_ref(self, state):
        if state:
            self.reg |= (1 << 1)
        else:
            self.reg &= 0b11111111_11111111_11111111_11111101
        self.update_asic()
        
    def active_dac(self, dac_nb):
        if dac_nb == 0:
            self.reg &= 0b11111111_11111111_11111111_11100011
        elif dac_nb > 3 or dac_nb < 0:
            exit(1)
        else:
            self.reg &= 0b11111111_11111111_11111111_11100011
            self.reg |= (1 << (1+dac_nb))
        self.update_asic()
        
    def set_dac_value(self, value):
        if value > 1023:
            exit(1)
        else:
            self.reg &= 0b11111111_11111111_10000000_00011111
            self.reg |= value << 5
        self.update_asic()
        
    def set_active_nmos(self, nb):
        if(nb > 63):
            exit(1)
        else:
            self.reg &= 0b11111111_11100000_01111111_11111111
            self.reg |= nb << 15
        self.update_asic()
        
    def read_dac(self):
        self.ser.write(bytes([0xab, 0x06]))
        time.sleep(2)
        return self.ser.read_until()
    
    def read_refs(self):
        self.ser.write(bytes([0xab, 0x05]))
        x = self.ser.read_until()
        y = self.ser.read_until()
        return x + y
    
class DMM():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('192.168.95.189', 5024))
        self.socket.settimeout(5)
        print(self.socket.recv(64))
        print(self.socket.recv(64))

    def write(self, cmd):
        self.socket.send('{}\r'.format(cmd).encode('utf-8'))
        
    def ask(self, cmd):
        self.write(cmd)
        self.socket.recv(300).decode('utf-8').strip()
        data = self.socket.recv(300).decode('utf-8').strip()
        data = data[:data.find('\r')]
        return data

if __name__ == "__main__":
    dmm = DMM()
    print(dmm.ask("*IDN?"))
    x =(dmm.ask("READ?"))
    print(x)
    x =(dmm.ask("READ?"))
    print(x)
        
    sr = SR()
    # sr.active_ref(True)
    # sr.active_ref(False)


    # nmos = 0l
    # print(nmos)
    # sr.set_active_nmos(nmos)
    # exit(1)
    for i in range(3):
    # i=0
        dac_results = list()
        sr.active_dac(i+1)
        for j in range(0,1024, 1):
            print(j)
            sr.set_dac_value(j)
            result = float(dmm.ask("READ?"))
            print(result)
            dac_results.append(result)

        with open("dac_results{}".format(i), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(dac_results)
