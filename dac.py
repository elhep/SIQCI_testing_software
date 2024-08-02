import csv

RELAY_IN_3723 = 22

class DACMeas():
    def __init__(self, switch_all_v, dmm, arduino, perform, debuf=False) -> None:
        self.dmm = dmm
        self.perform = perform
        self.arduino = arduino
        self.switch_all_v = switch_all_v
        self.switch_card = dmm.cards[1]
        assert self.switch_card.__class__.__name__ == "Model_3723_2B"

    def setup(self):
        self.switch_card.switch_channel(RELAY_IN_3723)

    def reset_relays(self):
        self.switch_card.open(RELAY_IN_3723)

    def meas(self):
        if not self.perform:
            pass
        else:
            self.setup()
            self.switch_all_v()
            for i in range(3):
                self.arduino.set_active_dac(i)
                results = list()
                for output_value in range(1024):
                    self.arduino.set_dac_output(output_value)
                    results.append(self.dmm.meas())
                self.save_data(results, i)
            self.reset_relays()

    def save_data(self, data, dac_nb):
        with open("results/dac{}".format(dac_nb), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)