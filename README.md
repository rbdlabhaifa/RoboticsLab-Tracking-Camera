# Robotics Lab - Self Tracking Camera Project
**University of Haifa Robotics Lab project.**

### Authors:
* [Yaad Rebhun](https://github.com/YaadR)
* [Regev Aloni](https://github.com/AloniRegev)

## Project description:
Identify and acquire the main character in a scene with a real time, one lens's camera.
Project files:
1. `PoseEstimationModule.py` - Identify an object and find landmarks
2. `PoseProject.py` - capture image, image object, and calculate object motion


## Run Me:
IDE: **PyCharm**
### Installations:

```
pip install opencv-python
pip install mediapipe 
pip install numpy
```

To run the code on the tello drone, install [tello directory.](https://github.com/damiafuentes/DJITelloPy)

### Libraries:
1. PoseEstimationModule.py :
   * `Mediapipe`- ML solution for real time detection object detection, used for pedestrian detection
   * `time` - Synchronizes and tracks real-time processes
   * `Numpy` - Perform matrix operations on an image.
2. PoseProject.py:
   * `argv from sys` - Passing arguments from external devices.
   * `opencv /cv2` - Library of programming functions mainly aimed at real-time CV
   * `time` - Synchronizes and tracks real-time processes
   * `PoseEstimationModule` – Our module
   * `Numpy` - Perform matrix operations on an image.
   * `Datetime` – Record implementation
   * `Tello form djitellopy` – Tello drone API
### Arguments:
The program recive 2 input argoments.
 * `argv[1]` – Capture input. `0`= Integrated camera; `1`= Drone; `<file_path>`= Read video file.
 * `argv[2]`- Draw symbols over the input. `True`/`False`

### Basic interapts:
#### Quit program:
You can quit by pressing `Esc` button. If the program is at ***drone mode*** the drone will land with the execution of this command.
#### Recording:
The program has video recording capabilities. Given the recording command, a red circle mark appears in the upper right corner of the window.
* `R` - start recording.
* `S` - stop recording.

## Modes:
1. ***Integrated camera mode*** - `argv[1]='0'`
* ![Integrated camera mode](MarkdownFiles/integrated_camera.gif)

2. ***Drone mode*** - `argv[1]='1'`
* ![Drone mode2](MarkdownFiles/drone_flight2.gif)
* ![Drone mode1](MarkdownFiles/drone_flight1.gif)


3. ***Read video/image file*** - `argv[1]=<file_path>`
* ![Drone mode1](MarkdownFiles/video_file.gif)

## Math & Logic operations:
#### 1. Rescale frame
Resize the image according to a given percentage ratio.
#### 2. Hotzones
Drawing perpendicular lines that maintain the pre borders of the frame, relative to acquired object or given values.
* The <span style="color:red">***red***</span> lines - marks an anomaly of the object from the allowed regions, position at body width from the edges of the frame.
* The <span style="color:yellow">***yellow***</span> lines - marks the place where we want the object to move if the red line was crossed. position at two body width away from the frame edges.
  * The line will collide the frame center, under no circumstances the yellow line will overlap each other

![HotZones](/MarkdownFiles/hotZones.png)

#### 3. Bounding box
framing the boundaries of the detected object. Calculated by the maximum length between the figure's shoulders and the figure's waist.
#### 4. Enquire object
For the purpose of inquiry the character. Padding with zeros all parts of the image that don’t contain the identified object.
at object detection, a counter ("adj") counts frames. As it find an object it crops a relative window, sized 1.8 times the figure bounding box size, pads the rest of the frame
with zeros and 'feeds' the detection algorithm with the cropped frame at subsequent
cycle .

![croped image](/MarkdownFiles/crop_image.png)

#### 5. Drone movement logic:
  * front – object to frame ratio. front >0.4 – move backward, front<0.2 - move
  forward
  * yaw – derive logic from Hotzones – while red line is cross, rotate towards the
  frame center until yellow line is cross back to approved zone
  * isUp – solution for Tello drone properties – gives minor up and down
  movement so the drone remain active (the Tello drone aborting after 15s of not
  receiving any orders)
  
## Objectives towards finalize product:
* Modularity - Option to run on a number of different devices.
* loading and running over raspberry pi
* Scalability - Supports the identification and inquire of multiple objects simultaneously.
* Robustness - resistance to extreme cases
* MediaPipe is Google's open source directory and therefore it is not legal to market the
product as is. at least in principle.
