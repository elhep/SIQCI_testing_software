# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from cmos import CMOSMeas, NMOSMeas
from arduino import Arduino
from ivref import IVRefMeas
from dac import DACMeas
import time

def init(vsup, arduino):
    '''
    vsup.switch_18v_on
    vsup.switch_45v_on

    '''
    pass

def run(vsup, dmm, arduino, switch_all_v):
    vsup    = vsup
    picoamp = ()
    arduino = arduino
    dmm     = dmm
    lakeshore = () #LakeShore()

    measurements = [        # do NOT comment any line. If you want to skip some measuremnts, change arg: perfom=False!!!
        CMOSMeas(switch_all_v, dmm, vsup, arduino, perform=True),# do NOT comment any line
        NMOSMeas(switch_all_v, dmm, vsup, arduino, perform=True), # do NOT comment any line
        IVRefMeas(switch_all_v, dmm, arduino, lakeshore, "V", perform=True), # do NOT comment any line
        IVRefMeas(switch_all_v, dmm, arduino, lakeshore, "I", perform=True), # do NOT comment any line
        DACMeas(switch_all_v, dmm, arduino, perform=True), # do NOT comment any line
        # leakage, # do NOT comment any line
    ]

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
    vsup = NGP800(channels_config=[ch1, ch2, ch3, ch4], ip="192.168.95.140", debug=True)

    arduino = Arduino(serial_nb=1, debug = True, sim = True)

    from keithley.Drivers.Series_3700A.Series_3700A_Python_Sockets_Driver import card_model, Series_3700A_Sockets_Driver
    def switch_all_v(state):
        if state:   # Arduino - first to swich on, last to swich off
            arduino.switch_vsup(state)
            vsup.output.general.set_state(state)
            time.sleep(1)
        else:
            vsup.output.general.set_state(state)
            arduino.switch_vsup(state)
            time.sleep(1)
    controler = Series_3700A_Sockets_Driver.KEI3706A(switch_all_v, stub=1)
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
    # card3732 = controler.cards[2]
    # card3732.close(card3732.channel_number(1, 2, 7))


    run(vsup, controler, arduino, switch_all_v)

