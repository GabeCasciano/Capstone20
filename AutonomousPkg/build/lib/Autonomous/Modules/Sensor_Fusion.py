from threading import *
import numpy as np
import time
from math import cos, sin, radians, degrees

from Autonomous.Sensors.IMU.IMU_Interface import IMU_Interface
from Autonomous.Sensors.GPS.GPS_Interface import GPS_Interface

class Sensor_Fusion(Thread):
    def __init__(self, IMU: IMU_Interface, GPS:GPS_Interface):

        super(Sensor_Fusion, self).__init__()

        self.__imu = IMU
        self.__gps = GPS

        # measurements are made relative to start conditions, the imu will be zeroed, and bias measured and compensated for
        # the reset function serves to reset all of the measurements and serve as the reference point.

        self.__global_acceleration_vector = np.array(["NaN", "NaN"], np.float32)
        self.__global_velocity_vector = np.array(["NaN", "NaN"], np.float32)
        self.__global_position_vector = np.array(["NaN", "NaN"], np.float32)
        self.__global_orientation = 0.0

        self.__position_vector = np.array(["NaN", "NaN"], np.float32)
        self.__acceleration_vector = np.array(["NaN", "NaN"], np.float32)
        self.__velocity_vector = np.array(["NaN", "NaN"], np.float32) 

        self.__gps_start_position = np.array(["NaN", "NaN"], np.float32)
        self.__gps_bearing = 0.0

        self.__v_log_start = 0

        self.__running = False

    # use the position functions to get the position relative to the start of fusion

    @property
    def gps_vector(self) -> list:
        return [self.__gps.latitude, self.__gps.longitude]

    @property
    def gps_longitude(self) -> float:
        return self.__gps.longitude

    @property
    def gps_latitude(self) -> float:
        return self.__gps.latitude

    @property
    def acceleration_x(self) -> float:
        return self.__global_acceleration_vector[0]

    @property
    def acceleration_y(self) -> float:
        return self.__global_acceleration_vector[1]

    @property
    def acceleration_vector(self) -> list:
        return self.__global_acceleration_vector.tolist()

    @property
    def velocity_x(self) -> float:
        return self.__global_velocity_vector[0]

    @property
    def velocity_y(self) -> float:
        return self.__global_velocity_vector[1]

    @property
    def velocity_vector(self) -> list:
        return self.__global_velocity_vector.tolist()

    @property
    def position_x(self) -> float:
        return self.__global_position_vector[0]

    @property
    def position_y(self) -> float:
        return self.__global_position_vector[1]

    @property
    def position_vector(self) -> list:
        return self.__global_position_vector.tolist()

    @property
    def orientation(self) -> float:
        return self.__global_orientation

    @property
    def running(self):
        return self.__running

    # control functions
    def calibrate(self) -> bool:
        self.__imu.do_calibration()
        self.__imu.set_lin_accel_rel()
        self.__imu.set_angular_pos_rel()
        self.__imu.set_angular_vel_rel()

    def reset(self):
        pass

    # thread functions
    def stop_thread(self):
        self.__running = False
        self.__imu.stop_thread()
        self.__gps.stop_thread()

    def start(self) -> None:
        if not self.__imu.running:
            self.__imu.start()
        if not self.__gps.running:
            self.__gps.start()

        self.__running = True

        self.__global_acceleration_vector = np.array([0, 0], np.float32)
        self.__global_velocity_vector = np.array([0, 0], np.float32)
        self.__global_position_vector = np.array(["NaN", "NaN"], np.float32)
        
        super(Sensor_Fusion, self).start()

    def run(self) -> None:

        self.__imu.do_calibration()
        self.__imu.set_lin_accel_rel()
        self.__imu.set_angular_vel_rel()
        self.__imu.set_angular_pos_rel()

        while self.__running:
            # if there is gps data waiting, read it into the sf (dead reconing)
            if self.__gps.new_data_flag:
                # collect cylindrical coords
                mag = GPS_Interface.haversin(self.__gps_start_position.tolist(), self.__gps.position)
                angle = radians(GPS_Interface.bearing_to(self.__gps_start_position.tolist(), self.__gps.position))

                # convert to cartesian
                self.__global_position_vector[0] = cos(angle) * mag
                self.__global_position_vector[1] = sin(angle) * mag

                self.__velocity_vector = np.array([0, 0], np.float32) # clear velocity logger
            else:  # if there is no gps data waiting, use the IMU
                # read the acceleration from the IMU, account for direction
                self.__global_acceleration_vector[0] = self.__imu.lin_accel[0] * cos(self.__imu.angular_pos[2])
                self.__global_acceleration_vector[1] = self.__imu.lin_accel[1] * sin(self.__imu.angular_pos[2])

                # read the orientation from the IMU, relative to the initial calibration
                self.__global_orientation = self.__imu.angular_pos[2]

                # Calculate velocity logger
                self.__velocity_vector += self.__global_acceleration_vector * (time.perf_counter() - self.__v_log_start)
                self.__global_velocity_vector = self.__velocity_vector.copy()

                # if the glbl pos has been initialized, calculate the position vector correction
                if self.__global_position_vector[0] != "NaN":
                    self.__global_position_vector += self.__velocity_vector * (time.perf_counter() - self.__v_log_start)

                self.__v_log_start = time.perf_counter()
