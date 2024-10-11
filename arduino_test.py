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
ser.write(bytes([0xab, 0x03, 0xab, 0x01, 0x00, 0x00, 0x00, 0x00]))

print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
while(True):
    print(ser.read_all())
#     ser.write(bytes([0xab, 0x02, 0x20]))
    input()
    time.sleep(1)
    ser.write(bytes([0xab, 0x01, 0x00, 0x00, 0x00, 0x00]))
