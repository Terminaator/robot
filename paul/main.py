from ai import ai
from vision import vision
from mainboard import mainboard

import serial
import time
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]
ser = serial.Serial(device, 115200, timeout=0.01)

field = 'A'
robot = 'A'
activated = 1

def respond():
    response = 'rf:a' + field + robot + 'ACK-----'
    ser.write(response.encode())
    
while True:
    #print(ser.read())
    ref_command = ser.read()
    if ref_command.startswith('<ref:a' + field + robot) or ref_command.startswith('<ref:a' + field + 'X'):
        command = ref_command[8:]
        if command == 'START----':
            activated = 1
            respond()
        if command == 'STOP-----':
            activated = 0
            respond()
        if command == 'PING-----':
            respond()
    if activated == 1:
        ai.start()
        vision.start()
        mainboard.start()
        ai.join()
        vision.join()
        mainboard.join()
        activated = 2
    elif activated == 0:
        ai.kill()
        vision.kill()
        mainboard.kill()
        activated = 2
    if ai.isalive() == False:
        print('dead')