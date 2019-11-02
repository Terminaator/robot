import time

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial("COM7", 115200, timeout=0.01)


while True:
    ser.write("d:1500\n".encode())
    time.sleep(1)
    ser.write("d:3000\n".encode())
    time.sleep(1)

