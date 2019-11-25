import time
from xml.etree.ElementTree import PI

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]
ser = serial.Serial(device, 115200)

while True:

    wheelSpeedToMainboardUnits = 90.9

    wheelAngularSpeedMainboardUnits = 2 * 90.9457

    wheelSpeedToMainboardUnits = 181.8914

    ser.write("sd:" + str(wheelSpeedToMainboardUnits) + ":" + wheelSpeedToMainboardUnits + ":10\n".encode())
    time.sleep(1)

