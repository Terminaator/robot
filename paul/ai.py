import time

from simple_pid import PID
from thread import Thread
from mainboard import mainboard

pid = PID(0.8, 0, 0.00001, setpoint=330)

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

        wheelspeed = int(pid(x_ball))
        print(wheelspeed)
        wheelspeed1 = int(pid(y_ball))
        print(wheelspeed1)



ai = AI()