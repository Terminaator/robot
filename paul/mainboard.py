import serial.tools.list_ports
from thread import Thread


class Mainboard(Thread):
    def __init__(self):
        Thread.__init__(self)
        ports = serial.tools.list_ports.comports()
        device = list(map(lambda port: port.device, ports))[0]

        self.ser = serial.Serial(device, 115200)
        self.last_command = None

    def on_message(self, msg):
        self.last_command = msg

    def on_tick(self):
        while self.ser.in_waiting:
            self.ser.read()
        if self.last_command is None:
            return
        print(self.last_command)

mainboard = Mainboard()
