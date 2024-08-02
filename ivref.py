BGP_RELAY_IN_3723 = 21
ICS_RELAY_IN_3723 = 20

class IVRefMeas():
    def __init__(self, switch_all_v, dmm, arduino, lakeshore, IV, perform) -> None:
        self.dmm = dmm
        self.perform = perform
        self.arduino = arduino
        self.lakeshore = lakeshore
        self.switch_card = dmm.cards[1]
        self.switch_all_v = switch_all_v
        assert self.switch_card.__class__.__name__ == "Model_3723_2B"
        if IV == "I":
            self.file = "results/current_ref"
            self.switch = ICS_RELAY_IN_3723
        elif IV == "V":
            self.file = "results/voltage_ref"
            self.switch = BGP_RELAY_IN_3723

    def setup(self):
        self.switch_card.switch_channel(self.switch)

    def reset_relays(self):
        self.switch_card.open(self.switch)

    def meas(self):
        if not self.perform:
            pass
        else:
            temp = list()
            meas = list()
            self.setup()
            self.switch_all_v(True)
            self.arduino.switch_ref(True)
            for _ in range(100): # TODO define number of measurements
                t0, meas0 = self.single_meas()
                temp.append(t0)
                meas.append(meas0)
            self.arduino.switch_ref(False)
            self.save_to_file(temp, meas)#, temp1, i)
            self.reset_relays()
            

    def single_meas(self):
        # t0 = self.lakeshore.get_temp()
        # self.switch_card.switch_channel(BGP_RELAY_IN_3723)
        # v0 = self.dmm.meeas()
        # self.switch_card.switch_channel(ICS_RELAY_IN_3723)
        t0 = self.lakeshore.get_temp()
        meas0 = self.dmm.meas()
        return t0, meas0#, t1, i0
    
    def save_to_file(self, temp0, meas):#, temp1, i):
        with open(self.file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(temp0)
            writer.writerow(meas)
        # with open("results/current_ref", 'w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(temp1)
        #     writer.writerow(i)