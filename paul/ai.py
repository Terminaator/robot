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
            self.last = "left"
        else:
            mainboard.send_message("stop")
        
        

            if self.last == "left":
                mainboard.send_message("stop")
                self.last = None
            else:
                if x < 240:
                    self.last = "right"
                    mainboard.send_message("right")
                elif x > 360:
                    self.last = "left"
                    mainboard.send_message("left")
                elif 240 < x < 360:
                    self.last = "up"
                    mainboard.send_message("up")
        print(self.last)

ai = AI()
