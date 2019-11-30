import threading
import time
import queue


class Thread(threading.Thread):
    def __init__(self, tick_speed=0.01):
        threading.Thread.__init__(self)

        self.message_queue = queue.Queue()
        self.tick_speed = tick_speed
        self.time_sleep = 0.02

    def send_message(self, msg):
        self.message_queue.put_nowait(msg)

    def run(self):
        while True:
            try:
                # Try to get a message from the message queue,
                # do nothing if the queue is empty
                self.on_message(self.message_queue.get_nowait())
            except queue.Empty:
                pass

            self.on_tick()
            time.sleep(self.time_sleep)
