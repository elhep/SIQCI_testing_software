from RsNgx import *
import time

class ChannelConfig():
    def __init__(self, alias, vamplitude, camplitude, vprotection=None, vlimit=None, climit=None):
        self.alias = alias
        self.vprotection = vprotection
        self.vamplitude = vamplitude
        self.vlimit = vlimit
        self.camplitude = camplitude
        self.climit = climit

class NGP800(RsNgx):
    def __init__(self, channels_config: [ChannelConfig]*4, ip=None, debug=False, echo=True):
        self.debug = debug
        self.channels = dict()
        self.echo = echo
        if not debug:
            RsNgx.__init__(self, 'TCPIP::'+ip+'::INSTR')
            self.utilities.reset()
            self.output.general.set_state(False)
            for idx, config in enumerate(channels_config):
                if config is None:
                    continue
                else:
                    self.channels[config.alias] = self.clone()
                    self.channels[config.alias].set_persistent_channel(idx+1)
        else:
            for idx, config in enumerate(channels_config):
                if config is None:
                    continue
                else:
                    self.channels[config.alias] = config

        for config in channels_config:
            if config is None:
                continue
            self.set_select(config.alias, True)
            if config.vprotection is not None:
                self.set_voltage_protection_state(config.alias, True)    #OVP
                self.set_voltage_protection_level(config.alias, config.vprotection)
            if config.vlimit is not None:   # Safety limits
                self.set_valimit_upper(config.alias, config.vlimit)
                self.set_alimit_state(config.alias, True)
            if config.climit is not None:
                self.set_calimit_upper(config.alias, config.climit)
                self.set_fuse_state(config.alias, True)
            self.set_vamplitude(config.alias, config.vamplitude)
            self.set_camplitude(config.alias, config.camplitude) #TODO check delays
            # todo verify configuration above
        if not debug:
            self.output.general.set_state(False)
            time.sleep(0.5)

    def set_fuse_state(self, ch, state):
        if self.debug:
            print(f'{ch} FUSE:STATe {state}')
        else:
            self.channels[ch].fuse.set_state(state)
            if self.echo:
                print(f'{ch} FUSE:STATe {state}')

    def set_vamplitude(self, ch, vol):
        if self.debug:
            print(f'{ch} SOURce:VOLTage:LEVel:IMMediate:AMPLitude {vol}')
        else:
            self.channels[ch].source.voltage.level.immediate.set_amplitude(vol)
            time.sleep(0.5)
            if self.echo:
                print(f'{ch} SOURce:VOLTage:LEVel:IMMediate:AMPLitude {vol}')

    def set_valimit_upper(self, ch, vol):
        if self.debug:
            print(f'{ch} SOURce:VOLTage:LEVel:IMMediate:ALIMit:UPPer {vol}')
        else:
            self.channels[ch].source.voltage.level.immediate.alimit.upper.set(vol)
            if self.echo:
                print(f'{ch} SOURce:VOLTage:LEVel:IMMediate:ALIMit:UPPer {vol}')

    def set_alimit_state(self, ch, state):
        if self.debug:
            print(f'{ch} SOURce:ALIMit:STATe {state}')
        else:
            self.channels[ch].source.alimit.set_state(state)
            if self.echo:
                print(f'{ch} SOURce:ALIMit:STATe {state}')

    def set_camplitude(self, ch, vol):
        if self.debug:
            print(f'{ch} SOURce:CURRent:LEVel:IMMediate:AMPLitude {vol}')
        else:
            self.channels[ch].source.current.level.immediate.set_amplitude(vol)
            if self.echo:
                print(f'{ch} SOURce:CURRent:LEVel:IMMediate:AMPLitude {vol}')

    def set_calimit_upper(self, ch, vol):
        if self.debug:
            print(f'{ch} SOURce:CURRent:LEVel:IMMediate:ALIMit:UPPer {vol}')
        else:
            self.channels[ch].source.current.level.immediate.alimit.upper.set(vol)
            if self.echo:
                print(f'{ch} SOURce:CURRent:LEVel:IMMediate:ALIMit:UPPer {vol}')

    def set_select(self, ch, state):
        if self.debug:
            print(f'{ch} OUTPut:SELect {state}')
        else:
            self.channels[ch].output.set_select(state)
            if self.echo:
                print(f'{ch} OUTPut:SELect {state}')

    def set_voltage_protection_state(self, ch, state):
        if self.debug:
            print(f'{ch} SOURce:VOLTage:PROTection:STATe {state}')
        else:
            self.channels[ch].source.voltage.protection.set_state(state)
            if self.echo:
                print(f'{ch} SOURce:VOLTage:PROTection:STATe {state}')

    def set_voltage_protection_level(self, ch, level):
        if self.debug:
            print(f'{ch} SOURce:VOLTage:PROTection:LEVel {level}')
        else:
            self.channels[ch].source.voltage.protection.set_level(level)
            if self.echo:
                print(f'{ch} SOURce:VOLTage:PROTection:LEVel {level}')