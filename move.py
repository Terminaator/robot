import time

from pynput import keyboard
import serial.tools.list_ports


ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200)
throw = False
def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    global throw
    print(ser.readline())
    if k == 'up':
        if throw:
            ser.write("sd:0:-10:10\nd:1500\n".encode())
        ser.write("sd:0:-10:10\n".encode())
    elif k == 'left':
        if throw:
            ser.write("sd:0:-5:-5\nd:1500\n".encode())
        ser.write("sd:0:-5:-5\n".encode())
    elif k == 'down':
        if throw:
            ser.write("sd:0:10:-10\nd:1500\n".encode())
        ser.write("sd:0:10:-10\n".encode())
    elif k == 'right':
        if throw:
            ser.write("sd:0:5:5\nd:1500\n".encode())
        ser.write("sd:0:5:5\n".encode())
    elif k == 'space':
        if throw:
            ser.write("sd:0:0:0\nd:1500\n".encode())
        ser.write("sd:0:0:0\n".encode())
    elif k == 'e':
        if throw:
            ser.write("sd:10:0:0\nd:1500\n".encode())
        ser.write("sd:10:0:0\n".encode())
    elif k == 'q':
        if throw:
            ser.write("sd:-10:0:0\nd:1500\n".encode())
        ser.write("sd:-10:0:0\n".encode())
    elif k == 'd':
        if throw:
            throw = False
        else:
            throw = True



lis = keyboard.Listener(on_press=on_press)
lis.start()

lis.join()