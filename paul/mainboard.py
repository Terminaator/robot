import time

import serial.tools.list_ports
from thread import Thread


class Mainboard(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Open serial port
        # self.serial = pyserial.open or something

        # Last command from AI, initially no command
        ports = serial.tools.list_ports.comports()
        device = list(map(lambda port: port.device, ports))[0]

        self.ser = serial.Serial(device, 115200)
        self.last_command = None

    def on_message(self, msg):
        print("mainboard received:", msg)
        self.last_command = msg

    def on_tick(self):
        while self.ser.in_waiting:
            self.ser.read()

        # Do nothing when no command has been received
        if self.last_command == None:
            return

        if self.last_command == 'up': #korras
            self.ser.write("sd:-20:0:20\n".encode())
        elif self.last_command == 'back': #korras
            self.ser.write("sd:20:0:-20\n".encode())
        elif self.last_command == 'stop':
            self.ser.write("sd:0:0:0\n".encode())
        elif self.last_command == 'left':
            self.ser.write("sd:-10:-10:-10\n".encode())
        elif self.last_command == 'right':
            self.ser.write("sd:10:10:10\n".encode())


mainboard = Mainboard()