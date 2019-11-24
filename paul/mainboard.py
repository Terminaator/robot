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

    def first_wheel_speed(self, first):
        self.first = first

    def second_wheel_speed(self, second):
        self.second = second

    def third_wheel_speed(self, third):
        self.third = third

    def on_message(self, msg):
        print("mainboard received:", msg)
        self.last_command = msg

    def on_tick(self):
        while self.ser.in_waiting:
            self.ser.read()

        # Do nothing when no command has been received
        if self.last_command == None:
            return
        print("sd:" + str(self.first) + ":" + str(self.second) + ":" + str(self.third) + "\n")
        self.ser.write("sd:" + str(self.first) + ":" + str(self.second) + ":" + str(self.third) + "\n".encode())


mainboard = Mainboard()
