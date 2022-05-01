# Collect Data
Run the ```collect_data.py``` program to collect data. 
It can be used with a remote viewing software to allow the driver to control the robot from a secondary computer.

This program is desinged to stop collecting data once the appropriate amount is collected (3200 datapoints). Assuming one is collecting on average 1 datapoint every 3 seconds, it should take around 2.5 hours of driving to collect the entire amount of data. 

To drive, use the ```w``` ```a``` ```s``` ```d``` keys for directional control, and the digits 1-9 for speed control. The space is a stop that is logged in the data collection system, and the key ```e``` triggers a stop that is not logged.

Note: When connecting to a remote viewing software such as VNC, be sure to boot the Raspberry Pi while it is connected to HDMI. This will cause the Raspberry Pi to use the full screen.
