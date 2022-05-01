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

def appendcsv(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


        
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
camera=webcam(wdir="/home/pi/Neuron/v3/data/images/")
motors=motors(22,23,24,25) #m1, m2, m3, m4



global kill
global access
access=threading.Lock()

kill=False
vidfeed = threading.Thread(target=broadcast, args=())
vidfeed.start()



os.makedirs("data", exist_ok=True) 
try:
    f=open('./data/train.csv','r')
    read=f.read()
    f.close()
    if read == '':
        write=['Img_ID','Mode','Speed']
        appendcsv('./data/train.csv',write)
except FileNotFoundError:
    write=['Img_ID','Mode','Speed']
    appendcsv('./data/train.csv',write)
    

    
datapoints=3200


camera.wdir="/home/pi/Neuron/v3/data/images/"

os.makedirs("./data/images/", exist_ok=True) 
dirs=os.listdir("./data/images/")
if "state.txt" in dirs:
    dirs.remove("state.txt")
imgs=[int(item.split(".")[0].split("_")[1]) for item in dirs]
if len(imgs)==0:
    maxtrainimg=0
else:
    maxtrainimg=max(imgs)

    
if not maxtrainimg==datapoints:
    try:
        with open(camera.wdir+"state.txt","r") as file:
            data=file.read()
            motors.setspeed(int(data[0]))
    except FileNotFoundError:
        motors.setspeed(5)
        with open(camera.wdir+"state.txt","w+") as file:
            buf=str(motors.getspeed())
            file.write(buf)


#Collect train data
imagenum=maxtrainimg
while imagenum<datapoints:
    imagenum+=1
    
       
    while True:
        move=input(str(imagenum)+" > ")
        if move not in ["w","s","a","d"," "] and not move.isnumeric():
            if move=="?":
                print("Speed: "+str(motors.speed-1))
            if move=="e":
                motors.stop_motors()
            continue
        
        if move.isnumeric():
            motors.setspeed(int(move)+1)
            with open(camera.wdir+"state.txt","w+") as file:
                buf=str(motors.getspeed()-1)
                file.write(buf)
            continue
        
        if move in ["w","s","a","d"," "]:
            #STOP immediately
            motors.stop_motors()
            break
        else:
            continue
        
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
    
    access.acquire()
    img=camera.read()
    access.release()        

    camera.saveread(img, "image_"+str(imagenum)+".png")
    write=[imagenum,motors.getmode(),motors.getspeed()]
    appendcsv('./data/train.csv',write)
        
    
camera.kill()
motors.stop()
del motors
kill=True
vidfeed.join()







