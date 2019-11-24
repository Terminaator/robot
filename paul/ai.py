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
        # Do nothing if vision state is not known
        if "closest_ball_coordinates" not in self.vision_state:
            return

        # Process vision state and decide action
        # then send motor speeds command to mainboard
        x = self.vision_state["closest_ball_coordinates"][0]
        y = self.vision_state["closest_ball_coordinates"][1]
        distance = self.vision_state["distance"]
        if x == 0 and y == 0:
            mainboard.send_message("left")
            self.last = "NO_BALL"
        else:
            if self.last == "NO_BALL":
                mainboard.send_message("stop")
                self.last = None
            elif x < 300:
                mainboard.send_message("left")
            elif x > 340:
                mainboard.send_message("right")
            elif 300 < x < 340 and distance < 0.8:
                mainboard.send_message("stop")
            elif 300 < x < 340:
                mainboard.send_message("up")
        print(self.last, x, y, distance)


ai = AI()
