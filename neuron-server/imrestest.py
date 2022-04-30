# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:26:34 2022

@author: Eric Buehler
"""
import requests

url = 'http://127.0.0.1:8000/im_size'
my_img = {'image': open('depthtest.png', 'rb')}
r = requests.post(url, files=my_img)

# convert server response into JSON format.
print(r.json())

url = 'http://127.0.0.1:8000/predict'
my_img = {'image': open('depthtest.png', 'rb')}
r = requests.post(url, files=my_img)

# convert server response into JSON format.
print(r.json())