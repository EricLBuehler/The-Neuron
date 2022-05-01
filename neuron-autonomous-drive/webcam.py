import cv2
import depthai as dai
import numpy as np
import os
                

class webcam():
    def __init__(self, wdir="/home/pi/Neuron", dims=(320, 240)):
        self.wdir = wdir
        self.alive = True
        self.dims = dims
        os.makedirs(self.wdir, exist_ok=True)

        # Closer-in minimum depth, disparity range is doubled (from 95 to 190):
        extended_disparity = False
        # Better accuracy for longer distance, fractional disparity 32-levels:
        subpixel = False
        # Better handling for occlusions:
        lr_check = True

        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define sources and outputs
        monoLeft = self.pipeline.create(dai.node.MonoCamera)
        monoRight = self.pipeline.create(dai.node.MonoCamera)
        self.depth = self.pipeline.create(dai.node.StereoDepth)
        xout = self.pipeline.create(dai.node.XLinkOut)

        xout.setStreamName("disparity")

        # Properties
        monoLeft.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoRight.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
        self.depth.setDefaultProfilePreset(
            dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
        self.depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
        self.depth.setLeftRightCheck(lr_check)
        self.depth.setExtendedDisparity(extended_disparity)
        self.depth.setSubpixel(subpixel)

        # Linking
        monoLeft.out.link(self.depth.left)
        monoRight.out.link(self.depth.right)
        self.depth.disparity.link(xout.input)

        self.read_ = self.read_raw()
        
        config = self.depth.initialConfig.get()
        config.postProcessing.speckleFilter.enable = True
        config.postProcessing.speckleFilter.speckleRange = 50
        config.postProcessing.temporalFilter.enable = True
        config.postProcessing.spatialFilter.enable = True
        config.postProcessing.spatialFilter.holeFillingRadius = 2
        config.postProcessing.spatialFilter.numIterations = 1
        config.postProcessing.thresholdFilter.minRange = 400
        config.postProcessing.thresholdFilter.maxRange = 15000
        config.postProcessing.decimationFilter.decimationFactor = 2
        self.depth.initialConfig.set(config)
        
                
        
        
        
        # Optional. If set (True), the ColorCamera is downscaled from 1080p to 720p.
        # Otherwise (False), the aligned depth is automatically upscaled to 1080p
        downscaleColor = True
        fps = 30
        # The disparity is computed at this resolution, then upscaled to RGB resolution
        monoResolution = dai.MonoCameraProperties.SensorResolution.THE_720_P
        
        queueNames = []
        
        # Define sources and outputs
        camRgb = self.pipeline.create(dai.node.ColorCamera)
        left = monoLeft
        right = monoRight
        stereo = self.pipeline.create(dai.node.StereoDepth)
        
        rgbOut = self.pipeline.create(dai.node.XLinkOut)
        disparityOut = self.pipeline.create(dai.node.XLinkOut)
        
        rgbOut.setStreamName("rgb")
        queueNames.append("rgb")
        disparityOut.setStreamName("disp")
        queueNames.append("disp")
        
        #Properties
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        camRgb.setFps(fps)
        if downscaleColor: camRgb.setIspScale(2, 3)
        # For now, RGB needs fixed focus to properly align with depth.
        # This value was used during calibration
        camRgb.initialControl.setManualFocus(130)
        
        left.setResolution(monoResolution)
        left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        left.setFps(fps)
        right.setResolution(monoResolution)
        right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        right.setFps(fps)
        
        stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        # LR-check is required for depth alignment
        stereo.setLeftRightCheck(True)
        stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
        
        # Linking
        camRgb.isp.link(rgbOut.input)
        left.out.link(stereo.left)
        right.out.link(stereo.right)
        stereo.disparity.link(disparityOut.input)
        

    def read_raw(self):
        frameRgb = None
        # Connect to device and start pipeline
        with dai.Device(self.pipeline) as device:

            # Output queue will be used to get the disparity frames from the outputs defined above
            q = device.getOutputQueue(
                name="disparity", maxSize=4, blocking=False)
            
            while True:
                if not self.alive:
                    break
                inDisparity = q.get()  # blocking call, will wait until a new data has arrived
                frame = inDisparity.getFrame()
                # Normalization for better visualization
                frame = (frame * (255 / self.depth.initialConfig.getMaxDisparity())).astype(np.uint8)

                # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
                frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                
                latestPacket = {}
                latestPacket["rgb"] = None
                latestPacket["disp"] = None
        
                queueEvents = device.getQueueEvents(("rgb", "disp"))
                for queueName in queueEvents:
                    packets = device.getOutputQueue(queueName).tryGetAll()
                    if len(packets) > 0:
                        latestPacket[queueName] = packets[-1]
        
                if latestPacket["rgb"] is not None:
                    frameRgb = latestPacket["rgb"].getCvFrame()
        
                    yield frame,frameRgb
                    
                
                yield frame,frameRgb

    def __del__(self):
        self.kill()

    def read(self):
        image = next(self.read_)[0]
        return image
    def read_rgb(self):
        image = next(self.read_)[1]
        return image
    
    def saveimg(self, imgname):
        image = next(self.read_)[1]
        image = cv2.resize(image, self.dims, interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.wdir+imgname, image)

    def saveread(self, image, imgname):
        cv2.imwrite(self.wdir+imgname, image)

    def kill(self):
        self.alive = False
        img=next(self.read_)
        
try:
    camera.kill()
    kill=True
    vidfeed.join()
except NameError:
    pass