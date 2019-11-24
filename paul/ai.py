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
            mainboard.first_wheel_speed(10)
            mainboard.second_wheel_speed(10)
            mainboard.third_wheel_speed(10)
            mainboard.send_message("left")
            self.last = "NO_BALL"
        else:
            if self.last == "NO_BALL":
                mainboard.first_wheel_speed(0)
                mainboard.second_wheel_speed(0)
                mainboard.third_wheel_speed(0)
                mainboard.send_message("left")
                self.last = None
            elif x < 300:
                mainboard.first_wheel_speed(50)
                mainboard.third_wheel_speed(80)
                mainboard.send_message("left")
            elif x > 340:
                mainboard.first_wheel_speed(80)
                mainboard.third_wheel_speed(50)
                mainboard.send_message("left")
            else:
                mainboard.first_wheel_speed(0)
                mainboard.third_wheel_speed(0)
                mainboard.send_message("left")
        print(self.last, x, y, distance)


ai = AI()
