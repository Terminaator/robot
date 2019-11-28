from thread import Thread
from mainboard import mainboard


class AI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.vision_state = {}
        self.last = None
        self.go_forward = 0

    def on_message(self, msg):
        self.vision_state = msg

    def get_thrower_speed_by_distance(self):
        return 0

    def on_tick(self):
        if "ball_coordinates" not in self.vision_state:
            return

        x_ball = self.vision_state["ball_coordinates"][0]
        y_ball = self.vision_state["ball_coordinates"][1]
        ball_distance = self.vision_state["ball_distance"]

        x_basket = self.vision_state["basket_coordinates"][0]
        y_basket = self.vision_state["basket_coordinates"][1]
        basket_distance = self.vision_state["basket_distance"]
        print(x_ball,y_ball)
        if x_ball == 0 and y_ball == 0:
            if 3.5 < basket_distance < 20:
                self.last = "NO_BALL_BASKET_GO"
            else:
                self.last = "NO_BALL"
        elif 250 < x_ball < 390 and y_ball > 350:
            if 330 < x_basket < 350:
                self.last = "STOP"
            elif x_basket < 330:
                self.last = "TURN_BASKET_BALL_0"
            elif x_basket > 350:
                self.last = "TURN_BASKET_BALL_1"
                # elif x_ball < 100:
                #    self.last = "MOVE_LEFT"
                # elif x_ball > 440:
                #    self.last = "MOVE_RIGHT"
        else:
            mainboard.omni_monition(x_ball, y_ball)
            self.last = "OMNIDIRECTIONAL"

        mainboard.on_message(self.last)


ai = AI()
