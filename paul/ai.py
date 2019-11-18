from thread import Thread
from mainboard import mainboard

class AI(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Initially vision state is unknown
        self.vision_state = {}

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
        if x == 0 and y == 0:
            mainboard.send_message("left")
        elif 240 < x < 360:
            print(self.vision_state["distance"])
            mainboard.send_message("up")
        else:
            mainboard.send_message("up")
            mainboard.send_message("right")


ai = AI()
