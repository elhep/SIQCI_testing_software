BGP_RELAY_IN_3723 = 21
ICS_RELAY_IN_3723 = 20

class IVRefMeas():
    def __init__(self, dmm, arduino, lakeshore, perform) -> None:
        self.dmm = dmm
        self.perform = perform
        self.arduino = arduino
        self.lakeshore = lakeshore
        self.switch_card = dmm.cards[1]
        assert self.switch_card.__class__.__name__ == "Model_3723_2B"

    def setup(self):
        pass

    def meas(self):
        if not self.perform:
            pass
        else:
            temp0 = list()
            v = list()
            temp1 = list()
            i = list()
            self.arduino.switch_ref(True)
            for _ in range(100): # TODO define number of measurements
                t0, v0, t1, i0 = self.single_meas()
                temp0.append(t0)
                v.append(v0)
                temp1.append(t1)
                i.append(i0)
            self.arduino.switch_ref(False)
            self.save_to_file(temp0, v, temp1, i)
            self.switch_card.open(ICS_RELAY_IN_3723)

    def single_meas(self):
        t0 = self.lakeshore.get_temp()
        self.switch_card.switch_channel(BGP_RELAY_IN_3723)
        v0 = self.dmm.meas()
        self.switch_card.switch_channel(ICS_RELAY_IN_3723)
        t1 = self.lakeshore.get_temp()
        i0 = self.dmm.meas()
        return t0, v0, t1, i0
    
    def save_to_file(self, temp0, v, temp1, i):
        with open("results/voltage_ref", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(temp0)
            writer.writerow(v)
        with open("results/current_ref", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(temp1)
            writer.writerow(i)