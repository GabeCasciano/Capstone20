import numpy as np
from serial import Serial, tools
from threading import *
from time import *
import atexit

class IMU_Interface(Thread):
    ANGLE_UNSIGNED = False
    ANGLE_SIGNED = True
    _version = 1.1
    _angle_sign = ANGLE_UNSIGNED

    def __init__(self, loc: str = '/dev/ttyUSB0', baud: int = 115200, angle_sign:bool=False):

        self.__imu_serial = Serial()
        self.__imu_serial.port = loc
        self.__imu_serial.baudrate = baud

        super(IMU_Interface, self).__init__()

        self._angle_sign = angle_sign

        # readings from the sensor directly
        self._lin_accel = np.array(["NaN", "NaN", "NaN"], np.float32)
        self._angular_pos = np.array(["NaN", "NaN", "NaN"], np.float32)
        self._angular_vel = np.array(["NaN", "NaN", "NaN"], np.float32)

        # relative offsets for each sensor reading
        self._rel_lin_accel = np.array([0.0, 0.0, 0.0], np.float32)
        self._rel_angular_pos = np.array([0.0, 0.0, 0.0], np.float32)
        self._rel_angular_vel = np.array([0.0, 0.0, 0.0], np.float32)

        # bias offsets
        self._bias_lin_accel = np.array([0.0, 0.0, 0.0], np.float32)
        self._bias_angular_pos = np.array([0.0, 0.0, 0.0], np.float32)
        self._bias_angular_vel = np.array([0.0, 0.0, 0.0], np.float32)

        self.running = True

        self._current_time = 0.0
        self._prev_time = 0.0
        self._sample_rate = 0.0

        atexit.register(self.exit_func)

    # Control Functions
    def stop_thread(self):
        self.running = False

    def exit_func(self):
        self.__imu_serial.close()

    def do_calibration(self):
        print("Hold IMU steady, please allow 10s for accurate calibration")
        accel = np.array([0.0, 0.0, 0.0], np.float32)
        pos = np.array([0.0, 0.0, 0.0], np.float32)
        vel = np.array([0.0, 0.0, 0.0], np.float32)

        accel_dif = accel.copy()
        pos_dif = pos.copy()
        vel_dif = vel.copy()

        duration = 10
        readings = 50

        for i in range(0, readings):
            accel += self._lin_accel - accel_dif
            pos += self._angular_pos - pos_dif
            vel += self._angular_vel - vel_dif

            accel_dif = accel.copy()
            pos_dif = pos.copy()
            vel_dif = vel.copy()

            sleep(duration/readings)

        self._bias_lin_accel = accel/readings
        self._bias_angular_pos = pos/readings
        self._rel_angular_vel = vel/readings

        print("Done calibrating sensor")
        print("Lin accel bias: ", self._bias_lin_accel)
        print("Angular pos bias: ", self._bias_angular_pos)
        print("Angular vel bias: ", self._bias_angular_vel)


    def __do_sample_rate(self):
        self._current_time = perf_counter()
        self._sample_rate = self._current_time - self._prev_time
        self._prev_time = self._current_time

    # Parsing functions
    def __parse_lin_accel(self, data: list):
        self._lin_accel[0] = float((data[3] << 8) | data[2]) / 32768 * 16
        self._lin_accel[1] = float((data[5] << 8) | data[4]) / 32768 * 16
        self._lin_accel[2] = float((data[7] << 8) | data[6]) / 32768 * 16


    def __parse_angular_vel(self, data: list):
        self._angular_vel[0] = float((data[3] << 8) | data[2]) / 32768 * 2000
        self._angular_vel[1] = float((data[5] << 8) | data[4]) / 32768 * 2000
        self._angular_vel[2] = float((data[7] << 8) | data[6]) / 32768 * 2000

    def __parse_angular_pos(self, data: list):
        self._angular_pos[0] = float((data[3] << 8) | data[2]) / 32768 * 180
        self._angular_pos[1] = float((data[5] << 8) | data[4]) / 32768 * 180
        self._angular_pos[2] = float((data[7] << 8) | data[6]) / 32768 * 180

    # Thread run functions
    def run(self) -> None:
        data_word = []
        self.__imu_serial.open()

        while self.running:
            data_char = int.from_bytes(self.__imu_serial.read(1), byteorder='little')
            if data_char == 0x55:
                data_word.append(data_char)
                while data_word.__len__() < 9:
                    data_char = int.from_bytes(self.__imu_serial.read(1), byteorder='little')
                    data_word.append(data_char)

                if data_word[1] == 0X51: # linear accel
                    self.__parse_lin_accel(data_word)
                    self.__do_sample_rate()

                elif data_word[1] == 0X52: # angular vel
                    self.__parse_angular_vel(data_word)

                elif data_word[1] == 0X53: # angular pos
                    self.__parse_angular_pos(data_word)
                data_word = []
        self.__imu_serial.close()

    # Getter & setter functions
    @property
    def active(self):
        return self._active


    @property
    def signed_angle(self):
        return self._angle_sign

    @signed_angle.setter
    def signed_angle(self, sign:bool):
        self._angle_sign = sign

    @property
    def version(self):
        return self._version

    @property
    def lin_accel_raw(self):
        return self._lin_accel

    @property
    def angular_pos_raw(self):
        return self._angular_pos

    @property
    def angular_vel_raw(self):
        return self._angular_vel

    @property
    def lin_accel(self):
        return (self._lin_accel - self._rel_lin_accel - self._bias_lin_accel)

    @property
    def angular_pos(self):
        pos = (self._angular_pos - self._rel_angular_pos - self._bias_angular_pos)
        if not self._angle_sign:
            for i in range(0, 3):
                if pos[i] < 0:
                    pos[i] += 360
        return pos

    @property
    def angular_vel(self):
        return (self._angular_vel - self._rel_angular_vel - self._bias_angular_vel)

    @property
    def rel_lin_accel(self) -> list:
        return self._rel_lin_accel.tolist()

    @rel_lin_accel.setter
    def rel_lin_accel(self, offsets: list):
        if offsets.__len__() == 3:
            self._rel_lin_accel = np.array(offsets, np.float32)

    @property
    def rel_angular_pos(self) -> list:
        return self._rel_angular_pos.tolist()

    @rel_angular_pos.setter
    def rel_angular_pos(self, offsets: list):
        if offsets.__len__() == 3:
            self._rel_angular_pos = np.array(offsets, np.float32)

    @property
    def rel_angular_vel(self) -> list:
        return self._rel_angular_vel.tolist()

    @rel_angular_vel.setter
    def rel_angular_vel(self, offsets: list):
        if offsets.__len__() == 3:
            self._rel_angular_vel = np.array(offsets, np.float32)

    @property
    def bias_lin_accel(self):
        return self._bias_lin_accel

    @property
    def bias_angular_pos(self):
        return self._bias_angular_pos

    @property
    def bias_angular_vel(self):
        return self._bias_angular_vel

    @property
    def sample_rate(self) -> float:
        return self._sample_rate

    # Data control functions
    def set_lin_accel_rel(self):
        self._rel_lin_accel = self._lin_accel.copy()

    def set_angular_pos_rel(self):
        self._rel_angular_pos = self._angular_pos.copy()

    def set_angular_vel_rel(self):
        self._rel_angular_vel = self._angular_vel.copy()

    def zero_lin_accel_rel(self):
        self._rel_lin_accel = np.zeros(self._rel_lin_accel.shape)

    def zero_angular_pos_rel(self):
        self._rel_angular_pos = np.zeros(self._rel_angular_pos.shape)

    def zero_angular_vel_rel(self):
        self._rel_angular_vel = np.zeros(self._rel_angular_vel.shape)
