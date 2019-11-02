import time

from pynput import keyboard
import serial.tools.list_ports


ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200)

def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'up':
        ser.write("sd:0:-10:10\nd:1500\n".encode())
    elif k == 'left':
        ser.write("sd:0:-5:-5\nd:1500\n".encode())
    elif k == 'down':
        ser.write("sd:0:10:-10\nd:1500\n".encode())
    elif k == 'right':
        ser.write("sd:0:5:5\nd:1500\n".encode())
    elif k == 'space':
        ser.write("sd:0:0:0\nd:1500\n".encode())
    elif k == 'd':
        ser.write("d:5000\n".encode())



lis = keyboard.Listener(on_press=on_press)
lis.start()

lis.join()