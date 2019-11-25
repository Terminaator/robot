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
            if 5 < basket_distance < 20:
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
            pass
        mainboard.send_message("command")


ai = AI()
