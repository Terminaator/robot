import threading
import time
import numpy as np
import cv2
import time
import pyrealsense2 as rs

class getFrames(threading.Thread):
    def run(self):
        print("{} started!".format(self.getName()))
        
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
        profile = pipeline.start(config)   
        print("{} finished!".format(self.getName()))
        
class findBasket(threading.Thread):
    def run(self):
        print("{} started!".format(self.getName()))
        
        
        
        print("{} finished!".format(self.getName()))
        
def main():
    thread1 = getFrames(name = "Thread-1")
    thread1.start()
    thread2 = findBasket(name = "Thread-2")
    thread2.start()
    
if __name__ == '__main__':
    main()