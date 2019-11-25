import time

import math
from math import sqrt, atan2, cos
from thread import Thread
from mainboard import mainboard


class AI(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Initially vision state is unknown
        self.vision_state = {}
        self.last = None
        self.wheelSpeedToMainboardUnits = 18.75 * 64 / (2 * math.pi * 0.035 * 60)

    def on_message(self, msg):
        # Received message, overwrite vision state
        self.vision_state = msg

    def angle(self, ball_x, ball_y):
        return math.degrees(math.atan((abs(ball_y - 240)) / (640 - ball_x)))

    def on_tick(self):
        if "ball_coordinates" not in self.vision_state:
            return

        x_ball = self.vision_state["ball_coordinates"][0]
        y_ball = self.vision_state["ball_coordinates"][1]
        ball_distance = self.vision_state["ball_distance"]

        x_basket = self.vision_state["basket_coordinates"][0]
        y_basket = self.vision_state["basket_coordinates"][1]
        basket_distance = self.vision_state["basket_distance"]

        robotSpeed = sqrt(x_ball * x_ball + y_ball * y_ball)

        robotDirectionAngle = self.angle(x_ball, y_ball)
        wheelLinearVelocity1 = 30 * cos(robotDirectionAngle - 0)
        wheelLinearVelocity2 = 30 * cos(robotDirectionAngle - 120)
        wheelLinearVelocity3 = 30 * cos(robotDirectionAngle - 240)

        mainboard.first_wheel_speed(10)
        mainboard.second_wheel_speed(10)
        mainboard.third_wheel_speed(10)

        mainboard.send_message(self.last)

ai = AI()
