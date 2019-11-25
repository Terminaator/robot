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
        self.wheelSpeedToMainboardUnits = 18.75 * 64 / (2 * math.pi * 0.035 * 60)

    def on_message(self, msg):
        # Received message, overwrite vision state
        self.vision_state = msg

    def calculateAngleBetweenRobotAndBall(self, ball_x, ball_y):
        return math.degrees(math.atan((abs(ball_y - 240)) / (640 - ball_x)))

    def getSpeed(self, angle, omega, speedLimit):
        wheelOne = int(round(speedLimit * self.wheelSpeedToMainboardUnits * (
            self.calculateOneWheelVelocity(self.wheelOneAngle, angle, 10, omega))))
        wheelTwo = int(round(speedLimit * self.wheelSpeedToMainboardUnits * (
            self.calculateOneWheelVelocity(self.wheelTwoAngle, angle, 10, omega))))
        wheelThree = int(round(speedLimit * self.wheelSpeedToMainboardUnits * (
            self.calculateOneWheelVelocity(self.wheelThreeAngle, angle, 10, omega))))
        return wheelOne, wheelTwo, wheelThree

    def on_tick(self):
        if "ball_coordinates" not in self.vision_state:
            return

        x_ball = self.vision_state["ball_coordinates"][0]
        y_ball = self.vision_state["ball_coordinates"][1]
        ball_distance = self.vision_state["ball_distance"]

        x_basket = self.vision_state["basket_coordinates"][0]
        y_basket = self.vision_state["basket_coordinates"][1]
        basket_distance = self.vision_state["basket_distance"]

        print(self.getSpeed(90 - self.calculateAngleBetweenRobotAndBall(x_ball, y_ball), 0, 0.07))


ai = AI()
