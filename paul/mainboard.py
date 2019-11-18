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
        # Do nothing when no command has been received
        if self.last_command == None:
            return

        if self.msg == 'left':
            self.ser.write("sd:0:-5:-5\n".encode())
        elif self.msg == 'right':
            self.ser.write("sd:0:5:5\n".encode())

mainboard = Mainboard()