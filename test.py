import time
from xml.etree.ElementTree import PI

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]
ser = serial.Serial("COM7", 115200)

while True:

    ser.write("d:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\n"
              "d:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\n"
              "d:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\n"
              "d:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nd:1500\nsd:0:0:0\nsd:0:0:0\nsd:0:0:0\nsd:0:0:0\nsd:0:0:0\n".encode())
    time.sleep(2)
