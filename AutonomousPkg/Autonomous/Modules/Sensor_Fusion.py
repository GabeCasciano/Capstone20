from threading import *
import numpy as np

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

        self.__position_vector = np.array(["NaN", "NaN"], np.float32)
        self.__acceleration_vector = np.array(["NaN", "NaN"], np.float32)
        self.__velocity_vector = np.array(["NaN", "NaN"], np.float32) 

        self.__gps_start_position = np.array(["NaN", "NaN"], np.float32)
        self.__gps_bearing = 0.0

        self.__running = False

    # use the position functions to get the position relative to the start of fusion

    @property
    def gps_longitude(self) -> float:
        return

    @property
    def gps_latitude(self) -> float:
        return

    @property
    def acceleration_x(self) -> float:
        return

    @property
    def acceleration_y(self) -> float:
        return

    @property
    def acceleration_vector(self) -> tuple:
        return

    @property
    def acceleration_components(self) -> tuple:
        return

    @property
    def velocity_x(self) -> float:
        return

    @property
    def velocity_y(self) -> float:
        return

    @property
    def velocity_vector(self) -> tuple:
        return

    @property
    def velocity_components(self) -> tuple:
        return

    @property
    def global_x(self):
        return 
    
    @property
    def global_y(self):
        return 
    
    @property
    def global_vector(self):
        return 
    
    @property
    def global_components(self):
        return 
    
    @property
    def position_x(self) -> float:
        return

    @property
    def position_y(self) -> float:
        return

    @property
    def position_vector(self) -> tuple:
        return

    @property
    def position_components(self) -> tuple:
        return

    # control functions
    def calibrate(self) -> bool:
        pass

    def reset(self):
        pass

    # thread functions
    def stop_thread(self):
        pass

    def start(self) -> None:
        if not self.__imu.running:
            self.__imu.start()
        if not self.__gps.running:
            self.__gps.start()

        self.__running = True

        self.__global_acceleration_vector = np.array(["NaN", "NaN"], np.float32)
        self.__global_velocity_vector = np.array(["NaN", "NaN"], np.float32)
        self.__global_position_vector = np.array(["NaN", "NaN"], np.float32)

    def run(self) -> None:
        pass

