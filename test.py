import time
from xml.etree.ElementTree import PI

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]
ser = serial.Serial(device, 115200)

while True:

    ser.write("sd:0:-10:10\nd:-1500\n".encode())

