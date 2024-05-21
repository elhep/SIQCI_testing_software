# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from cmos import cmos, startup

def init(vsup, arduino):
    '''
    vsup.switch_18v_on
    vsup.switch_45v_on

    '''
    pass

def run(vsup, dmm):
    vsup    = vsup
    picoamp = ()
    arduino = ()
    dmm     = dmm

    measurements = [
        cmos,
        # nmos,
        # vref,
        # iref,
        # dac,
        # leakage,
    ]
    startup(dmm, vsup) #here will be arduino TODO
    # init(vsup, arduino)

    for test in measurements:
        test(dmm, vsup, arduino, picoamp)




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
    vsup = NGP800(channels_config=[ch1, ch2, ch3, ch4], ip="192.168.95.186", debug=True)

    from keithley.Drivers.Series_3700A.Series_3700A_Python_Sockets_Driver import card_model, Series_3700A_Sockets_Driver
    controler = Series_3700A_Sockets_Driver.KEI3706A(stub=1)
    controler.add_new_card(1, card_model.Model_3723_2B)
    # card3723 = controler.cards[1]
    # card3723.switch_channel(912)
    # card3723.switch_channel(2)
    # card3723.close(5)
    controler.add_new_card(2, card_model.Model_3732_4B,
                           [(True,False),(True,False),(True,False),(True,False)])
    # card3732 = controler.cards[2]
    # card3732.close(card3732.channel_number(1, 2, 7))


    run(vsup, controler)

