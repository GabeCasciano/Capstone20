# Sensors

------

Note that then using these interface the specific ports for each device need to be setup in the specific run-time application for the specific machine being used. Since all devices used are serial, their address may change upon reboot and is required to be updated.

------

## Car Interface

start the interface using the `start` method, and poll or set values from the vehicle using it's class properties.

### Constructor:

Parameters:

- **loc** : string corresponding to the serial port used by the car (default: `/dev/ttyUSB0`)
- **baud** : baud rate of the serial connection (default: `9600`)

### Class Properties:

- **running** : used to check if the thread is still running or has stopped.
- **motor_speed** : used to get and set the desired speed for the car.
- **steering_angle** : used to get and set the desired steering angle for the car.
- **left_led** : used to get and set the state of the vehicles left front headlight.
- **right_led** : used to get and set the state of the vehicles right front headlight.

### Control Methods:

- **start** : start the thread, and perform the necessary handshake with the car controller
- **stop_thread** : stop the car, close the serial connection and stop the thread.

------

## IMU Interface

The IMU parses the data stream from the IMU into the data structures provided by the class. The interface also measures and compensates for the bias of the sensor, as well as include relative offset option for zero'ing.

### Constructor:

Parameters:

- **loc** : string corresponding to the serial port used by the car (default: `/dev/ttyUSB0`)
- **baud** : integer baud rate of the serial connection (default: `9600`)
- **angle_sign** : boolean used to set the interface to signed or unsigned angle. (default: `False`)

### Class Properties:

- **running** : used to check if the interface is still running or has been stopped.
- **signed_angle** : used  to get or set if the interface will operate in signed or unsigned mode
- **lin_accel** : get the adjust value for linear acceleration
- **angular_pos** :  get the adjust value for angular position
- **angular_vel** : get the adjust value for angular velocity
- **lin_accel_raw** : get the raw values for linear acceleration
- **angular_pos_raw** : get the raw values for angular position
- **angular_vel_raw** ; get the raw values for angular velocity
- **rel_lin_accel** : used to get or set the value used to offset the raw linear acceleration value
- **rel_angular_pos** : used to get or set the value used to offset the raw angular position value
- **rel_angular_vel** : used to get or set the values used to offset the raw angular velocity value
- **bias_lin_accel** : used to get the bias measurement for linear acceleration which is used in the adjustment calculation
- **bias_angular_pos** : used to get the bias measurement for angular position which is used in the adjustment calculation
- **bias_angular_vel** : used to get the bias measurement for angular velocity which is used in the adjustment calculation
- **sample_rate** : used to get the sample rate of the interface

### Control Methods:

- **start** : used to start the interface thread and begin communication with the IMU
- **stop_thread** : used to close the serial port to the IMU and stop the thread
- **do_calibration** : used to calibration the IMU adjustment calculations by measuring the intrinsic bias in the sensor
- **set_lin_accel_rel** : used to zero adjusted linear acceleration value by setting the relative value to the current reading.
- **set_angular_pos_rel** : used to zero adjusted angular position value by setting the relative value to the current reading.
- **set_angular_vel_rel** : used to zero adjusted angular velocity value by setting the relative value to the current reading.
- **zero_lin_accel_rel** : used to zero the relative value for linear acceleration (effectively resetting it)
- **zero_angular_pos_rel** : used to zero the relative value for angular position (effectively resetting it)
- **zero_angular_vel_rel** : used to zero the relative value for angular velcoity (effectively resetting it)

------

## GPS Interface

The GPS interface simply parses the GPS data stream from USB and wraps it in this class.

Constructor:

Parameters:

- **loc** : string corresponding to the serial port used by the car (default: `/dev/ttyACM0`)
- **baud** : integer baud rate of the serial connection (default: `4800`)

### Class Properties:

- **running** : used to check if the interface is still running or has stopped.
- **position** : used to get the current GPS reading as a tuple (latitude, longitude)
- **latitude** : used to get the current GPS reading for latitude
- **longitude** : used to get the current GPS reading for longitude
- **ground_speed** : used to get the current GPS reading for ground speed
- **gps_time** : used to get the current GPS reading for its local time
- **sample_rate** : used to get the rate at which the GPS is sampled (or refreshed)
- **new_data_flag** : used to indicate that the GPS reading has been refreshed. This flag is reset when the **position** class properties is checked.

### Control Methods:

- **start** : used to start the interface thread and begin communications with the GPS
- **stop_thread** : used to stop communications with the GPS and stop the thread

### General Methods:

- **haversin** : used to calculate the haversin distance between two positions (accounts for the curvature of the earth)
- **bearing_to** : used to calculate the bearing between two points relative to north
- **convert_min_to_decimal** : convert degrees minute second coordinate format to decimal degrees.

------

## LIDAR Interface

The LIDAR interface parses full scans from the sensor and places the in a LIFO stack such that the most recent data is always on the top. If more data is required for a filter it can be taken from the stack.

### Constructor:

Parameters:

- **loc** : string corresponding to the serial port used by the car (default: `/dev/ttyUSB1`)
- **baud** : integer baud rate of the serial connection (default: `9600`)
- **sample_rate** :  desired sample rate (default: `4000`)
- **scan_rate** : desired scan rate (default: `5.5`)
- **stack_depth** : desired data stack depth (default: `10` , measured in full scans)

### Class Properties:

- **running** : used to check if the interface is running or has stopped
- **max_distance** : used to get or set the maximum distance for the LIDAR's range filter
- **min_distance** : used to get or set the minimum distance for the LIDAR's range filter
- **sensor_health** : used to poll the LIDAR's sensor health
- **sensor_info** : used to poll the LIDAR's info (scan rate, sample rate, etc..)
- **sample_rate** : used to get or set the sample rate of the LIDAR
- **scan_rate** : used to get or set the scan rate of the LIDAR
- **pop_recent_scan** : used to pop and return the most recent scan off the top of the data stack
- **recent_scan** : used to peak at the most recent scan in the stack
- **stack** : used to get the entire data stack of scans.

### Control Methods:

- **start** : used to start communications with the LIDAR and begin the thread
- **stop_thread** : used to stop communications with the LIDAR and stop the thread
- **stop_sensor** : used to stop LIDAR from spinning
- **reset_sensor** : used to trigger the LIDAR's reset sequence
- **start_motor** : used to begin spinning the LIDAR



