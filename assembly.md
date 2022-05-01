# Assembly guide


![Neuron](/images/neuron.jpg)


1. Setup the Raspberry Pi with 64-Bit Raspberry Pi OS. Be sure to enable VNC and SSH.
2. Mount the OAK-D depth camera to the front of the robot, in such a way that it is centered and is facing forward. The USB-C connector on the bottom should be routed through a hole, and connected to the one of the Raspberry Pi's USB 3.0 ports.


![Neuron](/images/frontview.jpg)

 
3. Stack Raspberry Pi and battery pack, elevating the Raspberry Pi above the rest of the chassis. The Raspberry Pi stack should be directly behind the OAK-D camera.


![Neuron](/images/sideview.jpg)


5. Attach the breadboard directly behind the Raspberry Pi.
6. Solder the connectors for the motor controllers.
7. Attach the motor controllers to the breadboard so that the screw terminals hang off opposite sides of the breadboard (one motor controller will be left, one will be right)
8. For the left motor controller (when viewing from behind the robot), connect IN1 to GP23, and IN2 to GP22. 
9. Screw in the red motor wire to the side of the motor screw terminal that has the number 2, and the black wire on the other terminal. Attach a battery clip in the same way, so that the order, down to up, when viewed from the back of the robot is red-black-red-black.


![Neuron](/images/topview.jpg)


10. For the right motor controller(when viewing from behind the robot), connect IN1 to GP24, and IN2 to GP25. Repeat step 8 on this motor controller.
11. To begin driving, use [this](https://github.com/EricLBuehler/The-Neuron/tree/master/neuron-drive) guide to help you get started. If you wish to start autonomous driving, see [this](https://github.com/EricLBuehler/The-Neuron#getting-started) guide.
