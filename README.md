**AUTONOMOUS ROBOT**

It is a computer vision-based navigation system that combines real-time object detection, precise pose estimation, and robust inter-module communication. This project demonstrates advanced robotics concepts including camera calibration, coordinate transformations, and distributed system architecture using ROS(robotic operating system).

This project focuses on enabling autonomous navigation for a robot by combining deep learning-based object detection with camera-based pose estimation. The system allows the robot to understand its environment, estimate its own position and orientation, and make real-time navigation decisions using visual inputs from a camera.

![image](https://github.com/user-attachments/assets/ee631160-a50a-4543-9765-a5420815b105)

_1.Object Detection with YOLOv8_

We use YOLOv8 (You Only Look Once), a state-of-the-art deep learning model for object detection.

It enables the robot to identify landmarks or objects in its surroundings from a live video feed.

These objects act as reference points for navigation decisions.

A custom dataset of labeled images was used for training, and the model achieves high accuracy in real-time.

_2. Pose Estimation using PnP_

The system employs Perspective-n-Point (PnP) algorithms to estimate the 6-DoF pose (3D position + orientation) of the robot.

Pose estimation is achieved using a calibrated camera and known markers like a chessboard pattern.

OpenCV's solvePnP() function computes the camera's position relative to real-world coordinates, enabling precise localization.

_3. Camera Calibration_

To ensure accurate pose estimation, the camera undergoes intrinsic calibration to eliminate lens distortion.

Calibration matrices and distortion coefficients are used to correct the input frames before applying PnP.

_4. Communication via Sockets_

The estimated pose data is transmitted over a network using Python’s socket module (UDP).

This allows external systems (like decision-making modules or simulation environments) to access the robot’s pose in real-time.

_5. Robot Operating System (ROS) Integration_

The architecture is modularized using ROS (Robot Operating System).

ROS nodes handle separate tasks like video capture, pose estimation, detection, and data publishing.

ROS’s tf library is used for managing coordinate transforms between different reference frames (e.g., camera frame to base frame).

                          +--------------------------+
                          |     Camera Module        |
                          | (Video Stream + Capture) |
                          +-----------+--------------+
                                      |
                                      v
                          +--------------------------+
                          |  Preprocessing &         |
                          |  Distortion Correction   |
                          |  (OpenCV Calibration)    |
                          +-----------+--------------+
                                      |
                                      v
                  +------------------+-------------------+
                  |                                      |
                  v                                      v
      +------------------------+             +--------------------------+
      |   Object Detection     |             |     Pose Estimation      |
      |   (YOLOv8 Inference)   |             |   (PnP using OpenCV)     |
      +-----------+------------+             +------------+-------------+
                  |                                      |
                  v                                      v
        +---------+----------+                +----------+-----------+
        | Detected Landmarks |                | Camera Pose in 3D   |
        +---------+----------+                | (x, y, z, roll,...) |
                  |                           +----------+-----------+
                  v                                      |
         +--------+--------+                            |
         |    Navigation    |<--------------------------+
         |  Decision Logic  |
         +--------+--------+
                  |
                  v
        +---------+----------+
        |   ROS Publisher    |
        |  (Pose & Objects)  |
        +---------+----------+
                  |
                  v
        +---------+----------+
        |  UDP Socket Stream |
        | (To Other Systems) |
        +--------------------+


Camera Module captures live video and sends it to:

Preprocessing for distortion removal and grayscale conversion.

YOLOv8 detects objects or visual landmarks.

PnP algorithm estimates the robot’s 3D pose using known patterns (e.g., chessboard).

Both outputs are used by the Navigation Logic to make movement decisions.

ROS publishes relevant data and communicates it over UDP sockets to external systems or simulations.

![Screenshot 2025-06-11 170712](https://github.com/user-attachments/assets/47fb3075-7cc1-4d5e-bb9c-7dc1a6921863)


**Performance**

YOLOv8 mAP@0.5: ~92.4% on custom dataset of 2,000+ annotated images.

Pose Estimation Accuracy: ~1 cm in position and <2° in orientation error after calibration.

Processing Speed: Achieves real-time inference at 20+ FPS depending on system hardware.


**Applications**

Indoor autonomous navigation for mobile robots or drones.

Real-time mapping and localization in smart warehouses or factories.

Educational robotics and vision-guided robotic arms.
