from threading import *
from time import *

class SensorFusion_Interface(Thread):

    def __init__(self):
        self.imu
        self.gps

        super(SensorFusion_Interface, self).__init__()

    def do_static_calibration(self):
        pass

    def