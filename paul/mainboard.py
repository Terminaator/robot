import time

import serial.tools.list_ports
from thread import Thread


class Mainboard(Thread):
    def __init__(self):
        Thread.__init__(self)
        ports = serial.tools.list_ports.comports()
        device = list(map(lambda port: port.device, ports))[0]

        self.ser = serial.Serial(device, 115200)
        self.last_command = None
        self.first = 0
        self.second = 0
        self.third = 0
        self.thrower = 0

    def first_wheel_speed(self, first):
        self.first = first

    def second_wheel_speed(self, second):
        self.second = second

    def third_wheel_speed(self, third):
        self.third = third

    def on_message(self, msg):
        print("mainboard received:", msg)
        self.last_command = msg

    def throw(self, speed):
        self.thrower = speed

    def on_tick(self):
        while self.ser.in_waiting:
            self.ser.read()

        # Do nothing when no command has been received
        if self.last_command == None:
            return
        if self.thrower > 0 and self.last_command != 'THROW':
            self.thrower = 0
        string = "sd:" + str(self.first) + ":" + str(self.second) + ":" + str(self.third) + "\n"
        if self.thrower != 0:
            string += "d:1500\n"
        self.ser.write(string.encode())


mainboard = Mainboard()
