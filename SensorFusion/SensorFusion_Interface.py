from threading import *
from time import *
import atexit


class SensorFusion_Interface(Thread):

    def __init__(self):
        self.imu
        self.gps

        self.running = True

        self.pred_accel = []
        self.pred_vel = []
        self.pred_pos = []
        self.pred_orientation = []

        self.last_location = []


        super(SensorFusion_Interface, self).__init__()

        atexit.register(self.do_exit())

    def do_static_calibration(self):
        # calls the imu's static calibration
        pass

    def run(self) -> None:
        # call calibration function
        # get base gps values
        # zero imu if needed

        while self.running:
            # check if new gps data is available or new flag is set by gps (new data)
            # if true:
                # dead reackon the system and calculate the states
                # reset the velocity logger (if this is too frequent do every other)
            # if false:
                # predict the current location and states
            pass

    def stop_thread(self):
        self.running = False

    def do_exit(self):
        self.stop_thread()