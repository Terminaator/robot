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
            mainboard.first_wheel_speed(20)
            mainboard.second_wheel_speed(20)
            mainboard.third_wheel_speed(20)
            mainboard.send_message("turn")
            self.last = "NO_BALL"
        else:
            if self.last == "NO_BALL":
                mainboard.first_wheel_speed(0)
                mainboard.second_wheel_speed(0)
                mainboard.third_wheel_speed(0)
                mainboard.send_message("stop")
                self.last = None
            elif x < 250:
                mainboard.first_wheel_speed(-20)
                mainboard.second_wheel_speed(-20)
                mainboard.third_wheel_speed(-20)
                mainboard.send_message("left")
            elif x > 390:
                mainboard.first_wheel_speed(20)
                mainboard.second_wheel_speed(20)
                mainboard.third_wheel_speed(20)
                mainboard.send_message("right")
            elif 250 < x < 390:
                mainboard.first_wheel_speed(-40)
                mainboard.second_wheel_speed(0)
                mainboard.third_wheel_speed(40)
                mainboard.send_message("fwd")
            else:
                mainboard.send_message(None)
                

ai = AI()
