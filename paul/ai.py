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
        self.robot_speed_x = 0
        self.robot_speed_y = 0
        self.last = None
        self.wheelSpeedToMainboardUnits = 18.75 * 64 / (2 * math.pi * 0.035 * 60)
        self.wheelOneAngle = 2
        self.wheelTwoAngle = 131.1
        self.wheelThreeAngle = 232.9

    def on_message(self, msg):
        # Received message, overwrite vision state
        self.vision_state = msg

    def calculateAngleBetweenRobotAndBall(self, ball_x, ball_y):
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

        print(self.calculateAngleBetweenRobotAndBall(x_ball,y_ball))


ai = AI()
