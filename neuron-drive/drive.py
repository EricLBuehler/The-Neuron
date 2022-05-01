#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:17:12 2022

@author: pi
"""
from webcam import webcam
from motor import motors
from csv import writer
import time
import os
import cv2
import threading


        
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


global camera
camera=webcam(wdir="/home/pi/Neuron/v4/")
motors=motors(22,23,24,25) #m1, m2, m3, m4



global kill
global access
access=threading.Lock()

kill=False
vidfeed = threading.Thread(target=broadcast, args=())
vidfeed.start()



while True:
    move=input("> ")
    if move not in ["w","s","a","d"," "] and not move.isnumeric():
        if move=="?":
            print("Speed: "+str(motors.speed-1))
        continue
    
    if move.isnumeric():
        motors.setspeed(int(move)+1)
        with open(camera.wdir+"state.txt","w+") as file:
            buf=str(motors.getspeed()-1)
            file.write(buf)
        continue
    
    if move in ["w","s","a","d"," "]:
        if move=="w":
            motors.fwd()
        elif move=="s":
            motors.bwd()
        elif move=="a":
            motors.left()
        elif move=="d":
            motors.right()
        elif move==" ":
            motors.stop_motors()
        continue
    else:
        continue
    
camera.kill()
motors.stop()
del motors
kill=True
vidfeed.join()







