import copy

from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion
import math

class Path_Planning:

    hasArrived = False

    # These are arbitrary values that need to be calibrated
    max_velocity = 100
    max_acceleration = 100
    look_ahead_factor = 10
    path_radius = 0
    seek_offset = 3
    
    def __init__(self, lng, lat, sf: Sensor_Fusion):
        self.__SF = sf
        if not self.__SF.running:
            self.__SF.start()

        self._correction_vector = [0,0]

        self.destination_lng = dest_long
        self.destination_lat = dest_lat

        self.initial_lng = self.__SF.gps_longitude
        self.initial_lat = self.__SF.gps_latitude

        self.path = Path(self.initial_lng, self.initial_lat, self.destination_lng, self.destination_lat)


    def follow_path(self):
        dest = self.get_destination() #relative destination
        
        v = self.__SF.velocity_vector
        self.velocity = Point(v[0], v[1]) #saving velocity as point vector

        current_location = self.get_location()
        print("Current Location: ", self.print_point(current_location))        
        
        future_location = self.predict_location(current_location.x, current_location.y)
        print("Future Location: ", self.print_point(future_location))

        # Check if future position is within the radius of the path
        [normal_point, segment] = self.get_normal(future_location)
        print("Normal Point: ", self.print_point(normal_point))

        # distance between normal point and predicted location 
        dist = math.sqrt((future_location.x - normal_point.x) ** 2 + (future_location.y - normal_point.y) ** 2)
        
        # vehicle headed off path if dist is greater than the path radius
        if dist >= self.path_radius:
            
            correction_vector = self.get_correction_vector(current_location, normal_point, segment) 
            return correction_vector

        else:
            return [0,0]


    def predict_location(self, current_x, current_y):
        velocity_n = Point(self.velocity.x, self.velocity.y).normalize #normalize the velocity
        
        predict = copy.deepcopy(velocity_n)
        predict.mult(self.look_ahead_factor) #this can be calibrated to meters / distance if needed

        future_point = Point(current_x + predict.x, current_y + predict.y)
        
        return future_point
    
    
    def add_waypoint(self, lng, lat): 
        self.path.add_segment(lng, lat)
        seg = self.path.get_segments()
        
        i = 1
        for segment in seg:
            print("Segment: ", i)
            print('(',segment.p1.x, ",", segment.p1.y,') to (',segment.p2.x, ",", segment.p2.y,')') 
            i+=1
        return 0


    def get_destination(self): # get destination in relative coordinates
        destination_p = self.path.get_relative_point(self.destination_lng, self.destination_lat)
        return destination_p


    def get_location(self): # get current location in relative coordinates
        location_p = self.path.get_relative_point(self.SF.gps_longitude(), self.SF.gps_latitud())
        return location_p


    def get_normal(self,  future_p): # find normal point on the closest segment
        first_run = True
        shortest_dist = 0
        for segment in self.path.get_segments():
            start_p = segment.p1
            end_p = segment.p2

            start_to_future = Point(future_p.x - start_p.x, future_p.y - start_p.y)
            start_to_end = Point(end.x - start_p.x, end.y - start_p.y)
            start_to_end.normalize()

            dot = start_to_future.x * start_to_end.x + start_to_future.y * start_to_end.y
            start_to_end.mult(dot)

            temp_normal_point = Point(start_to_end.x + start_p.x, start_to_end.y + start_p.y)
            # add check for if point is on segment


            # need segment with shortest normal distance
            dist = math.sqrt((future_p.x - temp_normal_point.x) ** 2 + (future_p.y - temp_normal_point.y) ** 2)
            if first_run:
                normal_point = temp_normal_point
                closest_segment = segment
                shortest_dist = dist 
                first_run = False
            elif dist < shortest_dist:
                normal_point = temp_normal_point
                closest_segment = segment
                shortest_dist = dist
        
        return [normal_point, closest_segment]


    def get_correction_vector(self, current_p, normal_p, segment):
        # correction vector = desired location - velocity

        direction_vector = Point(segment.p2.x - segment.p1.x, segment.p2.y - segment.p1.y)
        direction_vector.normalize()
        direction_vector.mult(self.seek_offset) #this value should be calibrated

        target = Point(normal_p.x + direction_vector.x, normal_p.y + direction_vector.y)
        
        print("Target Point: " + self.print_point(target))

        desired = Point(target.x - current_p.x, target.y - current_p.y)
        desired_mag = desired.mag()
        desired.normalize()

        # arriving behaviours - slow down when close to target
        distance_threshold = 10 #Calibrate this!!
        if desired_mag < distance_threshold:
            factor = distance_threshold / desired_mag * self.max_velocity
            desired.mult(factor)
        else:
            desired.mult(self.max_velocity)

        correction_vector = Point(desired.x - self.velocity.x, desired.y - self.velocity.y)
        
        self._correction_vector = [correction_vector.x, correction_vector.y]
        return self._correction_vector


    def print_point(self, p):
        x = str(p.x)
        y = str(p.y)
        return "[" + x + ", " + y + "]"


    @property
    def correction_vector(self):
        return self._correction_vector

    # def follow_path(self, lat: float, long: float) -> tuple:
    #     return tuple(self._correction_vector)


class Path:

    def __init__(self, current_lng, current_lat, dest_lng, dest_lat):
        self.segments = []
        self._dest_long = dest_lng
        self._dest_lat = dest_lat
        self._initial_lng = current_lng
        self._initial_lat = current_lat

        relative_destination = self.get_relative_point(self._dest_lat, self._dest_long)
        relative_initial_point = self.get_relative_point(self._initial_lat, self._initial_lng)
        
        # initially creates path with only 2 points, waypoints can be added to path through path planning
        initial_segment = Segment(relative_initial_point, relative_destination)
        self.segments.append(initial_segment)


    def get_slope(self, desired_lng, desired_lat):
        m = (desired_lng - self._initial_lng) / (desired_lat - self._initial_lat)
        return m


    def get_relative_point(self, lng, lat):
        #setting initial position to (0,0) all points will be measured relative to this
        rel_x = lat - self._initial_lat
        rel_y = lng - self._initial_lng
        return Point(rel_x, rel_y)


    def add_segment(self, lng, lat): 
        p = self.get_relative_point(lng, lat)
        i = 0
        for segment in self.segments:
            if segment.p1.x < p.x < segment.p2.x:
                # create and add new segment at this point
                s1 = Segment(segment.p1, p)
                s2 = Segment(p, segment.p2)

                self.segments.remove(segment)
                self.segments.insert(i, s1)
                self.segments.insert(i+1, s2)
                
                return

            i += 1

    def get_segments(self) -> list:
        return self.segments

    @property
    def destination_long(self) -> float:
        return self._dest_long

    @property
    def destination_lat(self) -> float:
        return self._dest_lat

    # @property
    # def path(self): # returns the path
    #     self._generate_path()
    #     return

    # def _generate_path(self):
    #     pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        mag = math.sqrt(self.x ** 2 + self.y ** 2)
         self.x = self.x / mag
         self.y = self.y / mag

    def mult(self, num):
        self.x = self.x * num
        self.y = self.y * num

    def sub(self, point):
        self.x = self.x - point.x
        self.y = self.y - point.y

    def add(self, point):
        self.x = self.x + point.x
        self.y = self.y + point.y

    def mag():
        return math.sqrt((self.x) ** 2 + (self.y) ** 2)


class Segment: 
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def get_slope(self):
        return((self.p2.y - self.p1.y)/(self.p2.x - self.p1.x))

    def get_len(self):
        return(math.sqrt((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2))