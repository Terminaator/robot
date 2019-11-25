import time

import math
from math import sqrt, atan2, cos
from simple_pid import PID
from thread import Thread
from mainboard import mainboard

pid = PID(0.8, 0, 0.00001, setpoint=330)
pid.output_limits = (-30, 30)
toBallSpeed = PID(0.3, 0.00001, 0, setpoint=420)
rotateForBasketSpeed = PID(0.3, 0, 0, setpoint=320)
rotateForBallDuringOmni = PID(0.35, 0, 0, setpoint=320)


class AI(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Initially vision state is unknown
        self.vision_state = {}
        self.robot_speed_x = 0
        self.robot_speed_y = 0
        self.last = None

    def on_message(self, msg):
        # Received message, overwrite vision state
        self.vision_state = msg

    def get_robot_speed(self):
        return sqrt(self.robot_speed_x * self.robot_speed_x + self.robot_speed_y * self.robot_speed_y)

    def get_robot_direction_angle(self):
        return atan2(self.robot_speed_x, self.robot_speed_y)

    def get_wheel_linear_velocity(self, wheel_angle):
        return self.get_robot_speed() * cos(self.get_robot_direction_angle() - wheel_angle)

    def omnidirec(self, x, y, speed, omniWheel1Speed):
        try:
            robotDirectionAngle = int(math.degrees(math.atan((327 - x) / y)) + 90)
        except ZeroDivisionError:
            robotDirectionAngle = 0.1

        wheelLinearVelocity1 = int(-speed * math.cos(math.radians(robotDirectionAngle - self.wheelAngle1)))
        wheelLinearVelocity2 = int(-speed * math.cos(math.radians(robotDirectionAngle - self.wheelAngle2)))
        wheelLinearVelocity3 = int(-speed * math.cos(math.radians(robotDirectionAngle - self.wheelAngle3)))

        print(wheelLinearVelocity1)
        print(wheelLinearVelocity2)
        print(wheelLinearVelocity3)

    def on_tick(self):
        if "ball_coordinates" not in self.vision_state:
            return

        x_ball = self.vision_state["ball_coordinates"][0]
        y_ball = self.vision_state["ball_coordinates"][1]
        ball_distance = self.vision_state["ball_distance"]

        x_basket = self.vision_state["basket_coordinates"][0]
        y_basket = self.vision_state["basket_coordinates"][1]
        basket_distance = self.vision_state["basket_distance"]

        omniWheelSpeed = int(toBallSpeed(y_ball))
        omniWheel1Speed = int(rotateForBallDuringOmni(x_ball))
        self.omnidirec(x_ball,y_ball,omniWheelSpeed,omniWheel1Speed)

ai = AI()
