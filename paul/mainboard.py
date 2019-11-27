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
        self.thrower_speed = 1500
        self.last_command = None

        self.ticks = 0

    def on_message(self, msg):
        self.last_command = msg

    def angle(self, ball_x, ball_y):
        return math.degrees(math.atan2(320 - ball_x, 480 - ball_y))

    def set_speeds_wheels(self, speed1, speed2, speed3):
        self.speed_one = speed1
        self.speed_two = speed2
        self.speed_three = speed3

    def set_thrower_speed(self, speed):
        self.thrower_speed = speed

    def omni_monition(self, x_ball, y_ball):
        direction_angle = self.angle(x_ball, y_ball)

        self.speed_one = int(-40 * math.cos(math.radians(direction_angle - 120 + 90)))
        self.speed_two = int(-40 * math.cos(math.radians(direction_angle - 0 + 90)))
        self.speed_three = int(-40 * math.cos(math.radians(direction_angle - 240 + 90)))

        self.ticks = 3

    def set_speeds(self):
        if self.last_command == "NO_BALL_BASKET_GO":
            self.set_speeds_wheels(-40, 0, 40)
        elif self.last_command == "NO_BALL":
            self.set_speeds_wheels(10, 10, 10)
        elif self.last_command == "STRAIGHT":
            self.set_speeds_wheels(-40, 0, 40)
        elif self.last_command == "THROW_BALL":
            self.set_speeds_wheels(-40, 0, 40)
        elif self.last_command == "TURN_BASKET_BALL_0":
            self.set_speeds_wheels(0, -20, 0)
        elif self.last_command == "TURN_BASKET_BALL_1":
            self.set_speeds_wheels(0, 20, 0)
        elif self.last_command == "MOVE_LEFT":
            self.set_speeds_wheels(0, 20, -20)
        elif self.last_command == "MOVE_RIGHT":
            self.set_speeds_wheels(0, -20, 20)

    def on_tick(self):
        while self.ser.in_waiting:
            self.ser.read()

        if self.last_command is None:
            return


        thrower = ""
        if self.ticks < 0:
            thrower += "d:" + str(self.thrower_speed) + "\n"
            self.ticks -= 1
        else:
            self.set_speeds()
            thrower = "d:0\n"
        move = "sd:" + str(self.speed_one) + ":" + str(self.speed_two) + ":" + str(self.speed_three) + "\n"

        command = move + thrower
        print(command)

        self.ser.write(command.encode())


mainboard = Mainboard()
