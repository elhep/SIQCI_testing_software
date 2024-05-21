class Arduino():
    def __init__(self):
        self.usb = None
        self.asic_config = 0

    def set_nmos_channel(self, n):
        # reset current config for nmos channel:
        self.asic_config = self.asic_config & 0b1111_1111_1111_0000_0011_1111_1111_1111
        n = n & 63
        self.asic_config |= (n << 14)
        print(self.asic_config)

        # self.usb.sent(self.asic_config) #TODO

    def set_active_dac(self, n):
        self.asic_config = self.asic_config & 0b1111_1111_1111_1111_1111_1111_1111_0001
        n = n & 7
        self.asic_config |= (n << 1)
        print(self.asic_config)

        # self.usb.sent(self.asic_config) #TODO

    def set_dac_output(self, val):
        self.asic_config = self.asic_config & 0b1111_1111_1111_1111_1100_0000_0000_1111
        val = val & 0x3FF
        self.asic_config |= (val << 4)
        print(self.asic_config)

        # self.usb.sent(self.asic_config) #TODO

    def switch_to_vadj(self):
        # TODO drive IO to switch voltage source from R&S
        pass

    def switch_to_picoammeter(self):
        # TODO drive IO to switch voltage source from picoammeter
        pass