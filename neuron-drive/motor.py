#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 15:10:43 2022

@author: pi
"""

import RPi.GPIO as GPIO

class motors():
    def __init__(self,m1_1, m1_2, m2_1, m2_2):
        self.m1_1=m1_1
        self.m1_2=m1_2
        self.m2_1=m2_1
        self.m2_2=m2_2

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        #Motors
        GPIO.setup(self.m1_1,GPIO.OUT)
        self.pwm1=GPIO.PWM(self.m1_1,100)
        GPIO.setup(self.m1_2,GPIO.OUT)
        self.pwm2=GPIO.PWM(self.m1_2,100)
        GPIO.setup(self.m2_1,GPIO.OUT)
        self.pwm3=GPIO.PWM(self.m2_1,100)
        GPIO.setup(self.m2_2,GPIO.OUT)
        self.pwm4=GPIO.PWM(self.m2_2,100)
        
        self.speedm1_1=0
        self.speedm1_2=0
        self.speedm2_1=0
        self.speedm2_2=0
        
        self.pwm1.start(self.speedm1_1)
        self.pwm2.start(self.speedm1_2)
        self.pwm3.start(self.speedm2_1)
        self.pwm4.start(self.speedm2_2)
        
        self.speed=0
        self.mode=0
                
    def __del__(self):
        del self.pwm1
        del self.pwm2
        del self.pwm3
        del self.pwm4

    def start_pwms(self):
        self.speedm1_1=0
        self.speedm1_2=0
        self.speedm2_1=0
        self.speedm2_2=0
        
        self.pwm1.ChangeDutyCycle(self.speedm1_1)
        self.pwm2.ChangeDutyCycle(self.speedm1_2)
        self.pwm3.ChangeDutyCycle(self.speedm2_1)
        self.pwm4.ChangeDutyCycle(self.speedm2_2)
        
    def stop(self):
        self.speedm1_1=0
        self.speedm1_2=0
        self.speedm2_1=0
        self.speedm2_2=0
        
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm3.ChangeDutyCycle(0)
        self.pwm4.ChangeDutyCycle(0)
        GPIO.output(self.m1_1, GPIO.LOW)
        GPIO.output(self.m1_2, GPIO.LOW)
        GPIO.output(self.m2_1, GPIO.LOW)
        GPIO.output(self.m2_2, GPIO.LOW)
        
        self.mode=0
        
    def left(self):
        self.speedm1_1=2.5*self.speed
        self.speedm1_2=0
        self.speedm2_1=10*self.speed
        self.speedm2_2=0
        self.mode=1
            
        self.pwm1.ChangeDutyCycle(self.speedm1_1)
        self.pwm2.ChangeDutyCycle(self.speedm1_2)
        self.pwm3.ChangeDutyCycle(self.speedm2_1)
        self.pwm4.ChangeDutyCycle(self.speedm2_2)
        
        

    def right(self):
        self.speedm1_1=10*self.speed
        self.speedm1_2=0
        self.speedm2_1=2.5*self.speed
        self.speedm2_2=0
        self.mode=2
            
        self.pwm1.ChangeDutyCycle(self.speedm1_1)
        self.pwm2.ChangeDutyCycle(self.speedm1_2)
        self.pwm3.ChangeDutyCycle(self.speedm2_1)
        self.pwm4.ChangeDutyCycle(self.speedm2_2)
        
        
    
    def fwd(self):
        self.speedm1_1=10*self.speed
        self.speedm1_2=0
        self.speedm2_1=10*self.speed
        self.speedm2_2=0
        self.pwm1.ChangeDutyCycle(self.speedm1_1)
        self.pwm2.ChangeDutyCycle(self.speedm1_2)
        self.pwm3.ChangeDutyCycle(self.speedm2_1)
        self.pwm4.ChangeDutyCycle(self.speedm2_2)
        
        self.mode=3
    
    def bwd(self):
        self.speedm1_1=0
        self.speedm1_2=10*self.speed
        self.speedm2_1=0
        self.speedm2_2=10*self.speed
        self.pwm1.ChangeDutyCycle(self.speedm1_1)
        self.pwm2.ChangeDutyCycle(self.speedm1_2)
        self.pwm3.ChangeDutyCycle(self.speedm2_1)
        self.pwm4.ChangeDutyCycle(self.speedm2_2)
        
        self.mode=4
    
    def stop_motors(self):
        self.speedm1_1=0
        self.speedm1_2=0
        self.speedm2_1=0
        self.speedm2_2=0
        
        self.pwm1.ChangeDutyCycle(self.speedm1_1)
        self.pwm2.ChangeDutyCycle(self.speedm1_2)
        self.pwm3.ChangeDutyCycle(self.speedm2_1)
        self.pwm4.ChangeDutyCycle(self.speedm2_2)
        
        self.mode=0

    def getspeeds(self):
        return [self.speedm1_1, self.speedm1_2, self.speedm2_1, self.speedm2_2]
    
    def setspeed(self, speed):
        self.speed=speed
        
    def getspeed(self):
        return self.speed
    
    def getmode(self):
        return self.mode
        
        
        
        
        
        
        
        
        
        