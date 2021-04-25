# Autonomous Robot Sensors Package

------

This package contains all of the software and sensor interfaces required for a simple path following and obstacle detecting and avoiding robotic vehicle. The structure of the package is outlined below, however not outlined are the additional directories included in this package which include the build files as well as the distributable python package in both *whl* and *tar* formats, as well as a handful of scripts required to build and install the python package as well as clean the python environment if a version has already been installed.

------

**Autonomous**: The top-level directory for the python package.

- **Modules**: Contains all of the high-level algorithms required for this project.
  - **Obstacle_Detection.py**: This file implements an obstacle detection algorithm that is used to determine if obstacles obstruct the vehicles path, and determine their location relative to the vehicle.
  - **Obstacle_Avoidance.py**: This file implements an obstacle avoidance class and algorithm which simply navigates around the detected obstacle and returns the vehicle to its original path. 
  - **Path_Planning.py**: This file implements the primary path planning algorithm which generates the path, calculates the vehicles error and correction vector relative to the generated path.
  - **Sensor_Fusion.py**: This file implements a practical approach to an extended Kalman filter to fuse together GPS and IMU feedback into stable global coordinates and orientation. 
- **Run**: Contains all of the run-times.
  - **ManualControl.py**: This file implements manual control via bluetooth controller connected to the base-station computer. It uses an *Arcade control scheme* which is similar to many video games where one joystick controls both power and steering.
  - **GPSAuto.py**: This file implements a simple GPS autonomous, when run the vehicle will navigate to its destination using only the onboard GPS.
  - **SFAuto.py**: This file implements the sensor fusion autonomous, where the vehicle will use its fused IMU and GPS data to navigate from point to point.
  - **FullAuto.py**: This file implements the full autonomous system, where it will use the sensor fusion for position and orientation feedback as well as the LIDAR to detect and avoid obstacles.
- **Sensors**: Contains all of the sensor interfaces. Each interface implements a thread such that the sensor can be parsed and run concurrently to the rest of the system.
  - **Car**: Contains the interface and test files associated with the car.
    - **PS4_Controller**: Simple python thread used to read a bluetooth controller, meant for use with the manual control run-time.
    - **Car_Interface.py**: This file implements a thread which is used to communicate with the car's on board micro-controller, and provide it with instructions.
    - **Car_Test.py**: This file implements a simple test program which can be used to ensure the the *Car_Interface* is functioning correctly.
  - **GPS**: Contains all of the interface and test files associated with the GPS
    - **GPS_interface.py**: This file implements a thread which is used to parse information from the GPS, the thread is also responsible for formatting the GPS's data into appropriate data structures, providing control functions, as well as provide any conversion functions required. 
    - **GPS_Server.py**: This file implements a simple TCP server which is used to connect to the *GPS_Interface* remotely for control or to view what data is being parsed. 
    - **GPS_Test.py**: This file implements some simple tests to ensure that the *GPS_Interface* is working correctly.
  - **IMU**
    - **IMU_Interface.py**: This file implements a thread which is used to parse information from the IMU, the thread is responsible for formatting the IMU's data into appropriate data structures, as well as providing control functions.
    - **IMU_Server.py**: This file implements a simple TCP server which is used to connect to the *IMU_Interface* remotely for control or to view what data is being parsed.
    - **IMU_Test.py**: This file implements some simple tests to ensure that the *IMU_Interface* is working correctly.
  - **LIDAR**:
    - **LIDAR_Interface.py**: This file implements a thread which is used to parse information from the LIDAR, the thread is responsible for formatting the LIDAR's data into appropriate data structures, as well as providing control functions.
    - **LIDAR_Test.py**: This file implements some simple tests to ensure that the *LIDAR_Interface* is working correctly.
    - **LIDAR_Vis.py**: This file is used to visualise the data that the LIDAR  produces.



