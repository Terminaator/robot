from thread import Thread
from mainboard import mainboard


class AI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.vision_state = {}
        self.last = None
        self.go_forward = 0
        self.stop = True
        self.distances = {229: 1280, 169: 1300, 162: 1320, 132: 1380, 113: 1500, 410: 2150}

    def on_message(self, msg):
        self.vision_state = msg

    def get_closest_speed(self, y_basket):
        return min(self.distances, key=lambda x: abs(x - y_basket))

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
            print(x_ball, y_ball)
            if x_ball == 0 and y_ball == 0:
                if 3.5 < basket_distance < 20:
                    mainboard.omni_monition(x_basket, y_basket)
                    self.last = "OMNIDIRECTIONAL"
                else:
                    self.last = "NO_BALL"
            elif 300 < x_ball < 380 and y_ball > 350:
                if 330 <= x_basket <= 350 and y_ball > 400:
                    mainboard.omni_monition(x_basket, y_basket)
                    self.last = "OMNIDIRECTIONAL_THROW"
                if 330 <= x_basket <= 350:
                    self.last = "STRAIGHT_SLOW"
                elif x_basket < 330:
                    self.last = "TURN_BASKET_BALL_0"
                elif x_basket > 350:
                    self.last = "TURN_BASKET_BALL_1"
            else:
                mainboard.omni_monition(x_ball, y_ball)
                self.last = "OMNIDIRECTIONAL"

            mainboard.on_message(self.last)


ai = AI()
