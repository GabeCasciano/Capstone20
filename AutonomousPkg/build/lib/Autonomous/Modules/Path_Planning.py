from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion

class Path_Planning:

    def __init__(self, sensor_fusion: Sensor_Fusion):

        self._fusion = sensor_fusion

        self._start_x = 0
        self._start_y = 0

        self._end_x = 0
        self._end_y = 0

    def _check_sf_running(self) -> bool:
        return self._fusion.running

    def _start_sf(self):
        if not self._fusion.running:
            self._fusion.start()

    def set_start(self):
        self._start_sf()


