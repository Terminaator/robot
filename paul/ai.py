from thread import Thread
from mainboard import mainboard


class AI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.vision_state = {}
        self.last = None
        self.go_forward = 0
        self.stop = True

    def on_message(self, msg):
        self.vision_state = msg

    def get_thrower_speed_by_distance(self):
        return 0

    def on_tick(self):
        if not self.stop:
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
                    mainboard.omni_monition(x_basket, y_basket)
                    self.last = "OMNIDIRECTIONAL"
                else:
                    self.last = "NO_BALL"
            elif 300 < x_ball < 380 and 450 > y_ball > 350:
                if 330 < x_basket < 350:
                    if self.last == "STOP":
                        self.last = "THROW_BALL"
                    else:
                        self.last = "STOP"
                elif x_ball < 100:
                    self.last = "MOVE_LEFT"
                elif x_ball > 440:
                    self.last = "MOVE_RIGHT"
                elif x_basket < 320:
                    self.last = "TURN_BASKET_BALL_0"
                elif x_basket > 360:
                    self.last = "TURN_BASKET_BALL_1"
                else:
                    self.last = "STOP"

            else:
                mainboard.omni_monition(x_ball, y_ball)
                self.last = "OMNIDIRECTIONAL"

            mainboard.on_message(self.last)


ai = AI()
