import time

from thread import Thread
from mainboard import mainboard


class AI(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Initially vision state is unknown
        self.vision_state = {}
        self.last = None

    def on_message(self, msg):
        # Received message, overwrite vision state
        self.vision_state = msg

    def on_tick(self):
        if "ball_coordinates" not in self.vision_state:
            return

        x_ball = self.vision_state["ball_coordinates"][0]
        y_ball = self.vision_state["ball_coordinates"][1]
        ball_distance = self.vision_state["ball_distance"]

        x_basket = self.vision_state["basket_coordinates"][0]
        y_basket = self.vision_state["basket_coordinates"][1]
        basket_distance = self.vision_state["basket_distance"]

        if x_ball == 0 and y_ball == 0:
            if 3.5 < basket_distance < 20:
                mainboard.first_wheel_speed(-40)
                mainboard.second_wheel_speed(0)
                mainboard.third_wheel_speed(40)
                self.last = "NO_BALL_BASKET_GO"
            else:
                mainboard.first_wheel_speed(10)
                mainboard.second_wheel_speed(10)
                mainboard.third_wheel_speed(10)
                self.last = "NO_BALL"
        else:
            if self.last in ["NO_BALL_BASKET_GO", "NO_BALL"]:
                mainboard.first_wheel_speed(0)
                mainboard.second_wheel_speed(0)
                mainboard.third_wheel_speed(0)
                self.last = "BALL_FOUND"
            elif 250 < x_ball < 390:
                mainboard.first_wheel_speed(0)
                mainboard.second_wheel_speed(0)
                mainboard.third_wheel_speed(0)
                self.last = "FWD"
            elif x_ball < 250:
                speed = (250 - x_ball) / 28.9
                mainboard.first_wheel_speed(int(-speed))
                mainboard.second_wheel_speed(int(-speed))
                mainboard.third_wheel_speed(int(-speed))
                print(speed)
                self.last = "LEFT_BALL"
            elif x_ball > 390:
                speed = (x_ball - 390) / 28.9
                mainboard.first_wheel_speed(int(-speed))
                mainboard.second_wheel_speed(int(-speed))
                mainboard.third_wheel_speed(int(-speed))
                print(speed)
                self.last = "RIGHT_BALL"
        mainboard.send_message(self.last)


ai = AI()