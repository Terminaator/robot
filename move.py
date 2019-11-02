import time

import serial

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200, timeout=0.01)

while True:
    command = input("")

    ser.write("sd:1:1:1\n".encode())

    time.sleep(1)