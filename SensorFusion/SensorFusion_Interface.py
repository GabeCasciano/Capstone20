from threading import *
from time import *
import atexit
import numpy as np

from Sensors.IMU.IMU_Interface import *
from Sensors.GPS.GPS_Interface import *

class SensorFusion_Interface(Thread):

    def __init__(self, imu: IMU_Interface, gps: GPS_Interface, imu_forward: int = 0, imu_right: int = 1):
        self._imu = imu
        self._gps = gps

        self._imu_fwd = imu_forward
        self._imu_right = imu_forward

        super(SensorFusion_Interface, self).__init__()

        self._timer_start = 0.0
        self._timer = 0.0

        self._pred_pos = np.zeros(2)  # estimated global position
        self._pred_fwd_vel = 0.0

        self.running = True

        atexit.register(self.do_exit())

    # Class properties
    @property
    def ground_speed(self):
        return self._pred_fwd_vel

    @property
    def direction(self):
        return self._imu.angular_pos[self._imu.Z]

    @property
    def position(self):
        return

    @property
    def orientation(self):
        return

    @property
    def acceletation(self):
        return

    @@property
    def coordinates(self):
        return

    # Calculation functions
    def _do_velocity_logger(self):
        self._pred_fwd_vel += self._imu.lin_accel[self._imu_fwd] * perf_counter()

    def _do_timer(self):
        if self._timer_start == 0:
            self._timer_start = perf_counter()
        else:
            self._timer += perf_counter() - self._timer_start

    def _reset_timer(self):
        self._timer = 0.0
        self._timer_start = 0.0

    def _do_position_prediction(self):
        if self._gps.new_data_flag: # if there is new data up date via the gps and reset the velocity logger
            self._pred_pos[0] = self._gps.convert_decimal_to_meters(self._gps.longitude)
            self._pred_pos[1] = self._gps.convert_decimal_to_meters(self._gps.latitude)
            self._gps._new_data_flag = False
            self._pred_fwd_vel = 0.0
            self._reset_timer()
        else: # otw use the velocity logger
            self._pred_pos[0] += self._timer * self._pred_fwd_vel * sin(self._imu.angular_pos[self._imu.Z])
            self._pred_pos[1] += self._timer * self._pred_fwd_vel * cos(self._imu.angular_pos[self._imu.Z])

            # Calibration functions
    def _do_static_calibration(self):
        self._imu.do_calibration()
        sleep(11)

    # Control functions

    # Thread functions
    def run(self) -> None:
        # call calibration function
        # get base gps values
        # zero imu if needed
        self._do_static_calibration()
        self._imu.set_lin_accel_rel()
        self._imu.set_angular_pos_rel()
        self._imu.set_angular_vel_rel()

        while self.running:
            self._do_velocity_logger()
            self._do_position_prediction()

    def start(self) -> None:
        super(SensorFusion_Interface, self).start()
        self.running = True

    def stop_thread(self):
        self.running = False

    def do_exit(self):
        self.stop_thread()