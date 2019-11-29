import serial.tools.list_ports
import time
import threading

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200)


# define a thread which takes input
class InputThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            speed = input('input something: ')
            i = 40
            while i > 0:
                i -= 1
                ser.write(("d:" + str(speed) + "\n").encode())
                time.sleep(0.2)
            # do something based on the user input here
            # alternatively, let main do something with
            # self.last_user_input


# main
it = InputThread()
it.setDaemon(True)  # first
it.start()  # second
it.join()
