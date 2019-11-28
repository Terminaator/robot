from ai import ai
from vision import vision
from mainboard import mainboard

import serial
import time
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]
ser = serial.Serial(device, 115200, timeout=0.01)

field = 'X'
robot = 'Z'
activated = False

def respond():
    response = 'rf:a' + field + robot + 'ACK------\n'
    print(response)
    ser.write(response.encode())
    
command = ''
while True:
    #print(ser.read())
    ref_command = ser.read()
    respond()
    if ref_command.decode('ascii') == '\n':
        print(command)
            
        if command.startswith('<ref:a' + field + robot) or command.startswith('<ref:a' + field + 'X'):
            cmd = command[8:17]
            print('cmd=', cmd)

            if cmd == 'START----':
                activated = True
                # start AI
                respond()


            if cmd == 'STOP-----':
                # stop AI
                activated = False
                respond()
                    
            if cmd == 'PING-----':
                respond()

        command = ''
            

    else:
        command += ref_command.decode('ascii')

        """ if len(command) > 20:
            print(command)
            break """
        
        
        #print(str(activated)) - for checking if it works right or not
        
    time.sleep(0.01)
    #if activated == 1:
    #    ai.start()
    #    vision.start()
    #    mainboard.start()
    #    ai.join()
    #    vision.join()
    #    mainboard.join()
    #    activated = 2
    #elif activated == 0:
    #    ai.kill()
    #    vision.kill()
    #    mainboard.kill()
    #    activated = 2
    #if ai.isalive() == False:
    #    print('dead')
