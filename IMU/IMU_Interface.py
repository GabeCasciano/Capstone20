from serial import Serial
from serial import tools
from threading import *

class IMU_Interface(Thread):
    
    def __init__(self, loc: str = '/dev/ttyUSB0', baud: int = 115200):
        self.imu_serial = Serial()
        self.imu_serial.port = loc
        self.imu_serial.baudrate = baud

        super(IMU_Interface, self).__init__()

        self.lin_accel = [0, 0, 0]
        self.angular_pos = [0, 0, 0]
        self.angular_vel = [0, 0, 0]

    # --- Parsing thread ---

    def run(self) -> None:
        pass


    # --- Parsing Functions ---
    def parse_lin_accel(self, data:str):
        pass

    def parse_angular_vel(self, data:str):
        pass

    def parse_angular_pos(self, data:str):
        pass

    # --- Calculation Functions ---
    def do_velocity_logger(self):
        pass

    # --- Get Functions ---
    def get_linear_acceleration(self, axis:int = None):
        if axis < 3:
            return self.lin_accel[axis]
        return self.lin_accel

    def get_angular_orientation(self, axis:int = None):
        if axis < 3:
            return self.angular_pos[axis]
        return self.angular_pos
    # --- Control Functions ---