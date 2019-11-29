from ai import ai
from pynput import keyboard
from vision import vision
from mainboard import mainboard


def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    global throw
    if k == 'enter':
        ai.stop = not ai.stop
        mainboard.last_command = None

    if ai.stop:
        if k == "w":
            mainboard.last_command = "STRAIGHT"
        elif k == "a":
            mainboard.last_command = "MOVE_LEFT"
        elif k == "d":
            mainboard.last_command = "MOVE_RIGHT"
        elif k == "r":
            mainboard.last_command = "TURN_BASKET_BALL_0"
        elif k == "space":
            mainboard.last_command = "STOP"
        elif k == "s":
            mainboard.last_command = "BACK"



lis = keyboard.Listener(on_press=on_press)

lis.start()
ai.start()
vision.start()
mainboard.start()

lis.join()
ai.join()
vision.join()
mainboard.join()