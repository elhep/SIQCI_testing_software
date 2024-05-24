RELAY_IN_3723 = 22

class DACMeas():
    def __init__(self, dmm, arduino, perform, debuf=False) -> None:
        self.dmm = dmm
        self.perform = perform
        self.arduino = arduino
        self.switch_card = keithley_controller.cards[1]
        assert self.switch_card.__class__.__name__ == "Model_3723_2B"

    def setup(self):
        pass

    def meas(self):
        if not self.perform:
            pass
        else:
            self.switch_card.switch_channel(RELAY_IN_3723)
            for i in range(3):
                self.arduino.set_active_dac(i)
                results = list()
                for output_value in range(1024):
                    self.arduino.set_dac_output(output_value)
                    results.append(self.dmm.meas())
                self.save_data(results, i)
            self.switch_card.open(RELAY_IN_3723)

    def save_data(self, data, dac_nb):
        with open("results/dac{}".format(dac_nb), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)