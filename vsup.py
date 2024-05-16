from RsNgx import *

class NGP800(RsNgx):
    def __init__(self, ip):
        RsNgx.__init__(self, 'TCPIP::'+ip+'::INSTR')
        self.utilities.reset()
        self.output.general.set_state(False)
        self.channels = dict()
        self.channels["P45V0"] = self.clone()
        self.channels["P45V0"].set_persistent_channel(3)
        self.channels["P18V0"] = self.clone()
        self.channels["P18V0"].set_persistent_channel(1)
        self.channels["VADJ0"] = self.clone()
        self.channels["VADJ0"].set_persistent_channel(4)
        self.channels["VADJ1"] = self.clone()
        self.channels["VADJ1"].set_persistent_channel(2)
        for i, ch in enumerate(self.channels.values()):
            ch.output.set_select(True)
            # self.set_amplitude(ch, i)
            # ch.source.current.protection.set_state(True)
            ch.source.voltage.protection.set_state(True)
            ch.source.voltage.protection.set_level(13.5)
            ch.source.voltage.level.immediate.set_amplitude(12.0)
            ch.source.current.level.immediate.set_amplitude(1.0)
            ch.source.current.level.immediate.alimit.upper.set(4.0)
            ch.source.voltage.level.immediate.alimit.upper.set(13.5)
            ch.source.alimit.set_state(True)
            # ch._core.io.write(f'SOURce:CURRent:PROTection:STATe 1')
            # self._core.io.write(f'SOURce:CURRent:PROTection:STATe {param}')
            ch.fuse.set_state(True)

        #TODO set current limits, change voltage limit and voltage protection
        # ngx.source.voltage.protection.set_level()
        # ngx.source.voltage.level.immediate.alimit.upper.set(13.5)
        # ngx.source.current.set_range(arg_0=1.0)


    def set_amplitude(self, ch, vol):
        self.channels[ch].source.voltage.level.immediate.set_amplitude(vol)

    def set_select(self, ch, state):
        self.channels[ch].outputt.set_select(state)