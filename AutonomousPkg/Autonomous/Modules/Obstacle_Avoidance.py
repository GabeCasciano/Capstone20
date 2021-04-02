from Autonomous.Sensors.LIDAR import LIDAR_Interface, Utils
from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion

class Obstacle_Avoidance:

    def __init__(self):
        self.__running = False

    def avoid_obstacle(self, obstacle:tuple, direction:bool):
        # obstacle is the location of the obstacle relative to the robot
        # direction represents going to the left around the obstacle if false
        # uses the self.__running var to indicate that it is still running and to control the main while loop
        pass

    @property
    def running(self):
        return

    @property
    def duration(self):
        return