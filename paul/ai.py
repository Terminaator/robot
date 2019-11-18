from thread import Thread

class AI(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Initially vision state is unknown
        self.vision_state = {}

    def on_message(self, msg):
        # Received message, overwrite vision state
        print(2)
        self.vision_state = msg

    def on_tick(self):
        # Do nothing if vision state is not known
        pass