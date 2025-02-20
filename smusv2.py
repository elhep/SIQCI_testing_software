import time

from transistor_results import TResults, WD, SMU, SIQCI

dut = SIQCI()
dut.run_test("MUX", "NMOS", 2)
# dut._perform_transistor_test(id=3, asic=2, type="PMOS", bank=3.3)

exit()
