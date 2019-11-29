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
        print("OK")
    print(k)



lis = keyboard.Listener(on_press=on_press)
lis.start()

lis.join()
#ai.start()
#vision.start()
#mainboard.start()




#ai.join()
#vision.join()
#mainboard.join()