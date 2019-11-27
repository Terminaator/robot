from thread import Thread
from mainboard import mainboard


class AI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.vision_state = {}
        self.last = None

    def on_message(self, msg):
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
            self.last = "NO_BALL"
        elif 250 < x_ball < 390:
            self.last = "STRAIGHT"
        elif x_ball < 100:
            self.last = "MOVE_LEFT"
        elif x_ball > 440:
            self.last = "MOVE_RIGHT"
        else:
            mainboard.omni_monition(x_ball,y_ball)
            self.last = "OMNIDIRECTIONAL"
        mainboard.on_message(self.last)

ai = AI()
