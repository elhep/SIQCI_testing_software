import serial
import time

i = 0
while True:
    try:
        ser = serial.Serial(
            port = "COM" + str(i),
            baudrate=9600,
        )
        break
    except:
        i += 1
# ser.write(bytes([78]))
ser.write(bytes([0xab, 0x02, 0x20]))
print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
time.sleep(1)
ser.write(bytes([0xab, 0x02, 0x20]))
time.sleep(1)
input()
# ser.write(bytes([0xab, 0x03, 0xab, 0x01, 0x00, 0x00, 0x00, 0x00]))

print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
data_in = 0xd0
while(True):
    print(ser.read_all())
    input()
    time.sleep(1)
    # ser.write(bytes([0xab, 0x01, 0x00, 0x00, 0x00, 0x00])) #write register
    ser.write(bytes([0xab, 0x04]))
    # ser.write(bytes([0xab, 0x02, data_in]))
    # ser.write(bytes([0xab, 0x02, 0xb1]))
    # data_in += 1
    # ser.write(bytes([0xab, 0x02, data_in]))
    # data_in -= 1

