import math
import serial.tools.list_ports
from thread import Thread


class Mainboard(Thread):
    def __init__(self):
        Thread.__init__(self)
        ports = serial.tools.list_ports.comports()
        device = list(map(lambda port: port.device, ports))[0]

        self.ser = serial.Serial(device, 115200)
        self.speed_one = 0
        self.speed_two = 0
        self.speed_three = 0

        self.last_command = None

    def on_message(self, msg):
        self.last_command = msg

    def angle(self, ball_x, ball_y):
        return math.degrees(math.atan2(320 - ball_x, 480 - ball_y))

    def omni_monition(self, x_ball, y_ball):
        robotDirectionAngle = self.angle(x_ball, y_ball)

        self.speed_two = -40 * math.cos(math.radians(robotDirectionAngle - 0 + 90))
        self.speed_one = -40 * math.cos(math.radians(robotDirectionAngle - 120 + 90))
        self.speed_three = -40 * math.cos(math.radians(robotDirectionAngle - 240 + 90))

    def on_tick(self):
        while self.ser.in_waiting:
            #self.ser.read()
            print(self.ser.read())

        # Do nothing when no command has been received
        if self.last_command == None:
            self.ser.read()
        if self.last_command is None:
            return
        print(self.last_command)


mainboard = Mainboard()
