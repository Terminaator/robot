import time

from thread import Thread
from mainboard import mainboard

class AI(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Initially vision state is unknown
        self.vision_state = {}
        self.last = None
        self.isball = True

    def on_message(self, msg):
        # Received message, overwrite vision state
        self.vision_state = msg

    def is_ball(self):
        return self.isball


    def on_tick(self):
        # Do nothing if vision state is not known
        if "basket" in self.vision_state:
            x = self.vision_state["closest_ball_coordinates"][0]
            y = self.vision_state["closest_ball_coordinates"][1]
            distance = self.vision_state["distance"]
        elif "closest_ball_coordinates" in self.vision_state:
            x = self.vision_state["closest_ball_coordinates"][0]
            y = self.vision_state["closest_ball_coordinates"][1]
            distance = self.vision_state["distance"]

            if x == 0 and y == 0:
                mainboard.first_wheel_speed(10)
                mainboard.second_wheel_speed(10)
                mainboard.third_wheel_speed(10)
                mainboard.send_message("turn")
                self.last = "NO_BALL"
            else:
                if self.last == "NO_BALL":
                    mainboard.first_wheel_speed(0)
                    mainboard.second_wheel_speed(0)
                    mainboard.third_wheel_speed(0)
                    mainboard.send_message("stop")
                    self.last = None
                elif 250 < x < 390 and distance < 0.3:
                    print(x, y, distance)
                    mainboard.first_wheel_speed(0)
                    mainboard.second_wheel_speed(0)
                    mainboard.third_wheel_speed(0)
                    mainboard.send_message("fwd stop")
                    self.isball = False
                elif 250 < x < 390:
                    mainboard.first_wheel_speed(-40)
                    mainboard.second_wheel_speed(0)
                    mainboard.third_wheel_speed(40)
                    mainboard.send_message("fwd")
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
                else:
                    mainboard.send_message(None)
        else:
            return

ai = AI()
