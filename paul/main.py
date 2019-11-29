from ai import ai
from pynput import keyboard
from vision import vision
from mainboard import mainboard


def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    global throw
    if k == 'enter':
        ai.stop = not ai.stop
        mainboard.last_command = None
        mainboard.thrower_speed = 0



lis = keyboard.Listener(on_press=on_press)

lis.start()
ai.start()
vision.start()
mainboard.start()

lis.join()
ai.join()
vision.join()
mainboard.join()