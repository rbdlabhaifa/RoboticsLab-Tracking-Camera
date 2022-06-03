# RoboticsLab

##Project description:
Identify and acquire the main character in a scene with a real time, one lens's camera.
The project is divided into 2 main files:
1. `PoseEstimationModule.py` - Identify an object and find landmarks
2. `PoseProject.py` - capture image, image object, and calculate object motion


##Run Me:
IDE of choice: **PyCharm**
###Installations:

```
pip install opencv-python
pip install mediapipe 
pip install numpy
```

To run the code on the tello drone you need to additionally install the [tello directory.](https://github.com/damiafuentes/DJITelloPy)

###Libraries:
1. PoseEstimationModule.py :
   * `Mediapipe`- ML solution for real time detection object detection, used for pedestrian detection
   * `time` - Synchronizes and tracks real-time processes
   * `Numpy` - Perform matrix operations on an image.
2. PoseProject.py:
   * `argv from sys` - Passing arguments to a program to interface with external devices.
     * `argv[1]` – capture input. `0`= integrated camera; `1`= drone; `<file_path>`= read video file.
     * `argv[2]`- draw symbols over the input. `True`/`False`
   * `opencv /cv2` - library of programming functions mainly aimed at real-time computer vision
   * `time` - Synchronizes and tracks real-time processes
   * `PoseEstimationModule` – our module
   * `Numpy` - Perform matrix operations on an image.
   * `Datetime` – for record purposes
   * `Tello form djitellopy` – Tello drone API

##Math & Logic operations:
####1. Rescale frame
Resize the image according to a given percentage ratio.
####2. Hotzones
Drawing perpendicular lines that maintain the pre borders of the frame, relative to acquired object or given values.
* The <span style="color:red">**red**</span> lines - marks an anomaly of the object from the allowed regions, position at body width from the edges of the frame.
* The <span style="color:yellow">**yellow**</span> lines - marks the place where we want the object to move if the red line was crossed. position at two body width away from the frame edges.
  * The line will collide the frame center, under no circumstances the yellow line will overlap each other
####3. Bounding box
framing the boundaries of the detected object. Calculated by the maximum length between the figure's shoulders and the figure's waist.
####4. Enquire object
For the purpose of inquiry the character. Padding with zeros all parts of the image that don’t contain the identified object.
at object detection, a counter ("adj") counts frames. As it find an object it crops a relative window, sized 1.8 times the figure bounding box size, pads the rest of the frame
with zeros and 'feeds' the detection algorithm with the cropped frame at subsequent
cycle .
####5. Drone movement logic:
  * front – object to frame ratio. front >0.4 – move backward, front<0.2 - move
  forward
  * yaw – derive logic from Hotzones – while red line is cross, rotate towards the
  frame center until yellow line is cross back to approved zone
  * isUp – solution for Tello drone properties – gives minor up and down
  movement so the drone remain active (the Tello drone aborting after 15s of not
  receiving any orders)
  
##Objectives towards finalize product:
* Modularity - Option to run on a number of different devices.
* loading and running over raspberry pi
* Scalability - Supports the identification and inquire of multiple objects simultaneously.
* Robustness - resistance to extreme cases
* MediaPipe is Google's open source directory and therefore it is not legal to market the
product as is. at least in principle.






























The recent the update the upper it is.

## Milestone 4
### From object detection to acquire
![1](https://user-images.githubusercontent.com/85457983/168989953-469bc2a3-2854-4fbf-9b78-617296b667ac.PNG)
## Milestone 3
### Creating a diverse dataset and rescaling resolution & frame option
![1](https://user-images.githubusercontent.com/85457983/166112873-d9521e51-0e88-4cd2-83b3-602bb29c4858.JPG)
## Milestone 2
### Hotzpnes to determent the amount and direction of the camera to move to 
![image](https://user-images.githubusercontent.com/54915373/161993748-a10f035b-9f23-4ae9-b575-91572c3876b8.png)
## Milestone 1
### mediapipe detector - very good and accurate but not rectangle...
![image](https://user-images.githubusercontent.com/85457983/158022794-9a3b0be3-1f32-44e2-b6a0-b3084197dd4d.png)

### cv2 detertor - very slow and not very accurate, not sure why
![image](https://user-images.githubusercontent.com/85457983/158022758-4b684f36-2d91-4b3d-b51e-539dd785bf12.png)


