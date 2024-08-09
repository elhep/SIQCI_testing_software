import serial
import time

ser = serial.Serial(
    port = "/dev/ttyACM3",
    baudrate=9600,
)
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
ser.write(bytes([0xab, 0x01, 0x01, 0x02, 0x04, 0x08]))
print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
print(ser.read_all())
while(True):
    print(ser.read_all())
#     ser.write(bytes([0xab, 0x02, 0x20]))
    time.sleep(2)
#     print(ser.read_all())
#     time.sleep(2)
#     ser.write(bytes([0xab, 0x02, 0x20]))
#     time.sleep(2)
#     ser.write(bytes([78]))
#     print(ser.read_all())
#     time.sleep(2)