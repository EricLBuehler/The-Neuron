# The Neuron
### An autonomous robot, powered by AI.

Eric Buehler 2022



![Neuron](/images/neuron.jpg)


## Assembly
To build this robot, follow this [assembly guide](assembly.md).

## Getting started
Before starting for autonomous driving, check out [this](https://github.com/EricLBuehler/The-Neuron/tree/master/neuron-drive).

Click [here](https://github.com/EricLBuehler/The-Neuron/tree/master/neuron-collect_data) to begin.

## Parts

### Chassis
[Original Chassis](https://www.amazon.com/Platform-Powerful-Raspberry-Education-11-0x9-8x4-5inch/dp/B07MVYZHXD/ref=sr_1_22?dchild=1&keywords=raspberry%2Bpi%2Brobot%2Bchassis&qid=1591869810&sr=8-22&th=1)

However, this product is not currently available. Although any chassis can be used, [this](https://www.amazon.com/Chassis-Aluminum-Platform-Raspberry-Projects/dp/B078HQ5T5H/ref=sr_1_8?keywords=raspberry%2Bpi%2Brobot%2Bchassis&qid=1651366359&sr=8-8) is an alternate option. However, the assembly guide assumes that you are using the original chassis.

### Motor controller
**2X** [Motor controller](https://www.amazon.com/Adafruit-DRV8871-Motor-Driver-Breakout/dp/B06Y4VRXN4/ref=sr_1_2?dchild=1&keywords=Adafruit+DRV8871+DC+Motor+Driver+Breakout+Board+-+3.6A+Max&qid=1592953477&sr=8-2)

### Luxonis OAK-D camera
[Depth camera](https://www.amazon.com/Luxonis-Oak-D-Spatial-Camera-Detection/dp/B09B316YZS/ref=sr_1_3?keywords=depth+camera&qid=1646776703&sr=8-3)

### Raspberry Pi 4B - 8GB version
[Raspberry Pi 4B - 8GB](https://www.canakit.com/raspberry-pi-4-starter-kit.html)

### Connectors
- [Short USB-A to USB-C connector](https://www.amazon.com/CableCreation-Braided-Compatible-MacBook-Resistance/dp/B01CZVEUIE/ref=mp_s_a_1_1_sspa?dchild=1&keywords=usb+a+to+usb+c+short&qid=1591567443&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyMURQRk1QNDlZNEtKJmVuY3J5cHRlZElkPUEwNTc4MzIwM0FVNko0NjAxSUMzJmVuY3J5cHRlZEFkSWQ9QTA5NTI0MzkxVTkxQThMMkg0UzZCJndpZGdldE5hbWU9c3BfcGhvbmVfc2VhcmNoX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)

- [Battery clips](https://www.amazon.com/QMseller-Battery-I-Type-Connector-Plastic/dp/B07PPZXF5L/ref=sr_1_15?keywords=9V+battery+clip&qid=1651366664&sr=8-15)

### Batteries
- USB battery bank for the Raspberry Pi
- 2 9V batteries for each motor controller

### Miscellaneous
- 1 small Breadboard
- 4 jumper wires (female-male)



## References
[Perceiver IO: A General Architecture for Structured Inputs & Outputs](https://arxiv.org/abs/2107.14795)

[Perceiver: General Perception with Iterative Attention](https://arxiv.org/abs/2103.03206)

[Video explanation of Perceiver IO](https://www.youtube.com/watch?v=P_xeshTnPZg)

[GitHub implementation of PerceiverIO by Lucidrains](https://github.com/lucidrains/perceiver-pytorch)

[PerceiverIO classifier for MNIST](https://github.com/EricLBuehler/PerceiverIO-Classifier)
