from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion

class Path:

    def __init__(self): # change whatever parameters need to be changes or added
        self._correction_vector = [0,0]

    @property
    def correction_vector(self):
        return self._correction_vector

    def follow_path(self, lat: float, long: float) -> tuple:
        return tuple(self._correction_vector)


class Path_Planning:

    def __init__(self, dest_long: float, dest_lat: float):
        self._dest_long = dest_long
        self._dest_lat = dest_lat

    @property
    def destination_long(self):
        return self._dest_long

    @property
    def destination_lat(self):
        return self._dest_lat

    @property
    def path(self): # returns the path
        self._generate_path()
        return

    def _generate_path(self):
        pass



