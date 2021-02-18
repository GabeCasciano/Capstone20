# Gabriel Casciano, Feb 7, 2021

# Capestone 2020-2021

# This library is used to interface with the BWT61CL IMU to interface over the serial bus.
# This interface is multithreaded so it can run simultaneous to other interfaces and other
# system functionality

from serial import Serial
from serial import tools
from threading import *
import time

class IMU_Interface(Thread):
    
    def __init__(self, loc: str = '/dev/ttyUSB0', baud: int = 115200):
        self.imu_serial = Serial()
        self.imu_serial.port = loc
        self.imu_serial.baudrate = baud

        super(IMU_Interface, self).__init__()

        self.lin_accel = [0, 0, 0]
        self.angular_pos = [0, 0, 0]
        self.angular_vel = [0, 0, 0]

        self.rel_lin_accel = [0, 0, 0]
        self.rel_angular_pos = [0,0,0]
        self.rel_angular_vel = [0, 0, 0]

        self.vel_log = [0,0,0]

        self.running = True

        self.current_time = [0,0,0]
        self.prev_time = [0,0,0]
        self.sample_rate = [0,0,0]

    # --- Parsing thread ---

    def run(self) -> None:
        data_word = []
        self.imu_serial.open()

        while self.running:
            data_char = int.from_bytes(self.imu_serial.read(1), byteorder='little')
            if data_char == 0X55:
                data_word.append(data_char)
                while data_word.__len__() < 9:
                    data_char = int.from_bytes(self.imu_serial.read(1), byteorder='little')
                    data_word.append(data_char)

                if data_word[1] == 0X51: # linear accel
                    self.parse_lin_accel(data_word)
                    self.do_sample_rate(0)                  

                elif data_word[1] == 0X52: # angular vel
                    self.parse_angular_vel(data_word)
                    self.do_sample_rate(1)

                elif data_word[1] == 0X53: # angular pos
                    self.parse_angular_pos(data_word)
                    self.do_sample_rate(2)

                self.do_velocity_logger()
            data_word = []

        self.imu_serial.close()

    def do_sample_rate(self, command:int):
        self.current_time[command] = time.perf_counter()
        self.sample_rate[command] = self.current_time[command] - self.prev_time[command]
        self.prev_time[command] = self.current_time[command]

    def stop_thread(self):
        self.running = False
        
    # --- Parsing Functions ---
    def parse_lin_accel(self, data:list):

        self.lin_accel[0] = (((data[3] << 8)|data[2])/32768) * 16
        self.lin_accel[1] = ((data[5] << 8)|data[4])/32768 * 16
        self.lin_accel[2] = ((data[7] << 8)|data[6])/32768 * 16
        #self.temp = (((data[9] << 8)|data[8])/340) + 36.53
    
        #self.temp = self.rel_temp - self.temp
        #self.lin_accel = self.rel_lin_accel - self.lin_accel
        #self.lin_accel = [self.rel_lin_accel[i] - self.lin_accel[i] for i in range(0, 3)]

    def parse_angular_vel(self, data:list):
       
        self.angular_vel[0] = ((data[3] << 8)|data[2])/32768 * 2000
        self.angular_vel[1] = ((data[5] << 8)|data[4])/32768 * 2000
        self.angular_vel[2] = ((data[7] << 8)|data[6])/32768 * 2000

        # self.temp = (((data[9] << 8)|data[8])/340) + 36.53

        # self.temp = self.rel_temp - self.temp
        #self.angular_vel = self.rel_angular_vel - self.rel_angular_vel

        self.angular_vel = [self.rel_angular_vel[i] - self.angular_vel[i] for i in range(0,3)]

    def parse_angular_pos(self, data:list):
        self.angular_pos[0] = ((data[3] << 8)|data[2])/32768 * 180
        self.angular_pos[1] = ((data[5] << 8)|data[4])/32768 * 180
        self.angular_pos[2] = ((data[7] << 8)|data[6])/32768 * 180
        # self.temp = (((data[9] << 8)|data[8])/340) + 36.53

        # self.temp = self.rel_temp - self.temp
        #self.angular_pos = self.rel_angular_pos - self.lin_accel
        self.angular_pos = [self.rel_angular_pos[i] - self.angular_pos[i] for i in range(0,3)]

    # --- Calculation Functions ---
    def do_velocity_logger(self):
        self.vel_log += self.lin_accel

    # --- Get Functions ---
    def get_sample_rate(self, command:int=None):
        if command is not None:
            if command < 3:
                return self.sample_rate[command]
        return self.sample_rate

    def get_linear_acceleration(self, axis:int = None):
        if axis is not None:
            if axis < 3:
                return self.lin_accel[axis]
        return self.lin_accel

    def get_angular_orientation(self, axis:int = None):
        if axis is not None:
            if axis < 3:
                return self.angular_pos[axis]
        return self.angular_pos
    
    def get_angular_velocity(self, axis:int = None):
        if axis is not None:
            if axis < 3:
                return self.angular_vel[axis]
        return self.angular_vel

    # --- Zeroing Functions ---
    def zero_lin_accel(self):
        self.rel_lin_accel = self.lin_accel
    
    def zero_rel_lin_accel(self):
        self.rel_lin_accel = 0
        
    def zero_angular_pos(self):
        self.rel_angular_pos = self.angular_pos
    
    def zero_rel_angular_pos(self):
        self.rel_angular_pos = 0

    def zero_angular_vel(self):
        self.rel_angular_vel = self.angular_vel

    def zero_rel_angular_vel(self):
        self.rel_angular_vel = 0
    
    def zero_vel_log(self):
        self.vel_log = [0,0,0]