# Capstone20

By: Gabriel Casciano, Niha Shetty, Yasamin Ahmadzadeh, Mai Abdelhameed

An autonomous subsystem for a self-driving vehicle. Included in this project are the required software to interface with all of the autonomous sensors, algorithms and feedback loops which utilise the data from the sensors, and the different run-time applications which choose the specific algorithms for the given mode. 



## Project Structure

- **AutonomousPkg**: The custom python package written for this project.
  - **Autonomous**: The top-level directory for the python package.
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
  - **build.sh** & **clear.sh**: These two scripts can be used to build the python package, and clear a pre-installed version of the package from the python environment.
  - misc. build and distribution files.
- **ControlSystem**: The PCB and software designed and written to test the implementation of our algorithms on a vehicle.
- **Documents**: Implementation notes, diagrams, and documentation.
- **setup.sh**: This script can be used to install the required python packages into a python environment.



## Installation

To install the provided python package, python must first be [downloaded & installed](https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tar.xz). 

**From snap:**

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
```

**From source:**

```bash
wget -o https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tar.xz
tar xf Python-3.9.4
cd Python-3.9.4/configure
make
sudo make install
```

After completing the installation of python navigate to the top-level folder of this repository (this folder) and run the following script which contains all the required commands to build and install the python package in your local python environment, the package can also be installed in a python venv.

If the folder has not yet been downloaded it can be cloned with git:

```bash
git clone https://github.com/GabeCasciano/Capstone20.git
```

After that:

```bash
cd Capstone20/
./setup.sh
```

