# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from cmos import CMOSMeas, NMOSMeas
from arduino import Arduino
from ivref import IVRefMeas
from dac import DACMeas
import time

class PowerManagement():
    def __init__(self, arduino, vsup):
        self.arduino = arduino
        self.vsup = vsup

    def switch_all_v(self, state):
        if state:   # Arduino - first to swich on, last to swich off
            self.arduino.switch_vsup(state)
            time.sleep(1)
            self.vsup.output.general.set_state(state)
            time.sleep(1)
        else:
            self.vsup.output.general.set_state(state)
            self.arduino.switch_vsup(state)
            time.sleep(1)

def init(vsup, arduino):
    '''
    vsup.switch_18v_on
    vsup.switch_45v_on

    '''
    pass

def run(vsup, dmm, arduino, pwr):
    vsup    = vsup
    picoamp = ()
    arduino = arduino
    dmm     = dmm
    lakeshore = () #LakeShore()

    measurements = [        # do NOT comment any line. If you want to skip some measuremnts, change arg: perfom=False!!!
        CMOSMeas(pwr, dmm, vsup, arduino, perform=True),# do NOT comment any line
        NMOSMeas(pwr, dmm, vsup, arduino, perform=True), # do NOT comment any line
        IVRefMeas(pwr, dmm, arduino, lakeshore, "V", perform=True), # do NOT comment any line
        IVRefMeas(pwr, dmm, arduino, lakeshore, "I", perform=True), # do NOT comment any line
        DACMeas(pwr, dmm, arduino, perform=True), # do NOT comment any line
        # leakage, # do NOT comment any line
    ]

    arduino.switch_vsup(True)

    if not os.path.exists("results"):
        os.makedirs("results")

    print("\n::::::::::::::::::::::::::::::::::::::::::::::::")
    print("Connect USB to Arduino and press y")
    print("::::::::::::::::::::::::::::::::::::::::::::::::\n")
    x = input()
    while x != 'y':
        print("Press y after connecting USB to Arduino")
        x = input()

    for meas in measurements:
        meas.meas()




if __name__ == '__main__':
    from vsup import NGP800, ChannelConfig
    # First channel:
    ch1 = ChannelConfig(
        "P18V0",
        18.0,
        0.5,
        vprotection= 18.5,
        vlimit = 18.5,
        climit = 0.5
    )
    ch2 = ChannelConfig(
        "VADJ1",
        0.0,
        0.5,
        vprotection= 18.5,
        vlimit = 18.5,
        climit = 0.5
    )
    ch3 = ChannelConfig(
        "P45V0",
        45.0,
        0.5,
        vprotection= 45.5,
        vlimit = 45.5,
        climit = 0.5
    )
    ch4 = ChannelConfig(
        "VADJ0",
        0.0,
        0.5,
        vprotection= 45.5,
        vlimit = 45.5,
        climit = 0.5
    )
    vsup = NGP800(channels_config=[ch1, ch2, ch3, ch4], ip="192.168.95.140", debug=False)

    arduino = Arduino(serial_nb=1, debug = True, sim = False)

    pwr = PowerManagement(arduino, vsup)

    from keithley.Drivers.Series_3700A.Series_3700A_Python_Sockets_Driver import card_model, Series_3700A_Sockets_Driver

    controler = Series_3700A_Sockets_Driver.KEI3706A(pwr, echo=1, stub=0)
    ipAddress1 = "192.168.95.141"
    port = 5025
    timeout = 20.0
    myID = controler.Connect(ipAddress1, 5025, 20000, 1, 1)
    controler.add_new_card(1, card_model.Model_3723_2B)
    # card3723 = controler.cards[1]
    # card3723.switch_channel(912)
    # card3723.switch_channel(2)
    # card3723.close(5)
    controler.add_new_card(2, card_model.Model_3732_4B,
                           [(True,False),(True,False),(True,False),(True,False)])
    controler.SendCmd("channel.setbackplane(\"{}\",\"{}\")".format("1001:1030", str(1911)))
    controler.SendCmd("dmm.setconfig(\"{}\",\"{}\")".format("1001:1030", "dcvolts"))
    controler.SendCmd("BCVBuffer = dmm.makebuffer(1)")
    controler.SendCmd("dmm.measurecount = 1")
    # card3732 = controler.cards[2]
    # card3732.close(card3732.channel_number(1, 2, 7))


    run(vsup, controler, arduino, pwr)

