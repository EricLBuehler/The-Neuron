from webcam import webcam
import time
import os
import cv2
import threading
from motor import motors
import requests



def broadcast():
    time.sleep(5)
    while True:
        access.acquire()
        image=camera.read_rgb()
        access.release()
        cv2.imshow("RGB Video feed",image)
        access.acquire()
        image=camera.read()
        access.release()
        cv2.imshow("Depth Video feed",image)
        if cv2.waitKey(1) & 0xFF == ord('q') or kill:
            cv2.destroyWindow("RGB Video feed")
            cv2.destroyWindow("Depth Video feed")
            break



global kill
kill=False
global camera
camera=webcam(wdir="/home/pi/Neuron/v5/")


global access
access=threading.Lock()

vidfeed = threading.Thread(target=broadcast, args=())
vidfeed.start()
motors=motors(22,23,24,25) #m1, m2, m3, m4

"""
Left=1
Right=2
Fwd=3
Bwd=4
Stop=0
"""

motors.setspeed(5)

ip="192.168.1.157"

n=0
while True:
    access.acquire()
    image=camera.read()
    access.release()
    camera.saveread(image, "input.png")

    print("Requesting...")
    url = 'http://'+str(ip)+':8000//predict'
    img = {'image': open('input.png', 'rb')}
    r = requests.post(url, files=img).json()
    
    # convert server response into JSON format.
    #print(r)
    timediff=r['time_s']
    move=r['pred']
        
    if move=="forward":
        motors.fwd()
    elif move=="backward":
        motors.bwd()
    elif move=="left":
        motors.left()
    elif move=="right":
        motors.right()
    elif move=="stop":
        motors.stop_motors()
        
    print(f"Prediction #{n+1} took {timediff} s.")
    n+=1











