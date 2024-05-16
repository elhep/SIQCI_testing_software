# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def cmos():
    NotImplemented()

def init(vsup, arduino):
    '''
    vsup.switch_18v_on
    vsup.switch_45v_on

    '''
    NotImplemented()

def main():
    vsup    = ()
    picoamp = ()
    arduino = ()
    dmm     = ()

    measurements = [
        cmos,
        nmos,
        vref,
        iref,
        dac,
        leakage,
    ]

    init(vsup, arduino)

    for test in measurements:
        test(vsup, picoamp, arduino, dmm)




if __name__ == '__main__':
    from keithley.Drivers.Series_3700A.Series_3700A_Python_Sockets_Driver import card_model, Series_3700A_Sockets_Driver
    controler = Series_3700A_Sockets_Driver.KEI3706A(stub=1)
    controler.add_new_card(1, card_model.Model_3723_2B)
    card3723 = controler.cards[1]
    card3723.switch_channel(912)
    card3723.switch_channel(2)
    # card3723.close(5)
    controler.add_new_card(2, card_model.Model_3732_4B,
                           [(True,False),(True,False),(True,False),(True,False)])
    card3732 = controler.cards[2]
    card3732.close(card3732.channel_number(1, 2, 7))


    from vsup import NGP800
    vsup = NGP800("192.168.95.186")


