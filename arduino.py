import serial
SHDN = 2
REL1 = 3
REL0 = 2

class Arduino():
    def __init__(self, debug=False, sim = True):
        self.usb = None
        self.asic_config = 0
        self.debug = debug
        self.sim = sim
        if not sim:
            self.ser = serial.Serial('/dev/ttyUSB' + str(nb), 115200, timeout=2)

    def print_config(self):
        print("\nNew ASIC config:")
        print(bin(self.asic_config))
        print("\n")

    def _update_asic_reg(self):
        if not self.sim:
            self.ser.write(bytes([0xAB, 0x01]))

        data = list()
        for i in range(4):
            data.append((self.asic_config >> ((3-i)*8)) & 0xFF)

        if not self.sim:
            self.ser.write(bytes(data))

        if self.debug:
            print(" New ASIC REG bytes:")
            print(data)

    def _update_io_status(self, pin, value):
        if not self.sim:
            self.ser.write(bytes([0xAB, 0x02]))
        
        data = [((pin & 0xF) << 4) | (value & 0xF)]
        if not self.sim:
            self.ser.write(bytes(data))
        
        if self.debug:
            print(" New Arduino IO value:")
            print(data)

    def set_nmos_channel(self, n):
        # reset current config for nmos channel:
        self.asic_config = self.asic_config & 0b1111_1111_1111_0000_0011_1111_1111_1111
        n = n & 63
        self.asic_config |= (n << 14)
        if self.debug:
            self.print_config()
        self._update_asic_reg()

    def set_active_dac(self, n):
        self.asic_config = self.asic_config & 0b1111_1111_1111_1111_1111_1111_1111_0001
        n = n & 3
        self.asic_config |= (1 << n)
        if self.debug:
            self.print_config()
        self._update_asic_reg()

    def set_dac_output(self, val):
        self.asic_config = self.asic_config & 0b1111_1111_1111_1111_1100_0000_0000_1111
        val = val & 0x3FF
        self.asic_config |= (val << 4)
        if debug:
            self.print_config()
        self._update_asic_reg()

    def switch_to_vadj(self):
        self._update_io_status(REL1, 0) # VADJ to bank 3 and 4 of 3732 (not only bank 4) 
        self._update_io_status(REL0, 0) # source: R&S (not picoameter)

    def switch_to_picoammeter(self):
        self._update_io_status(REL0, 1) # source: picoameter (not R&S), remember to control REL1 for bank4 measurements