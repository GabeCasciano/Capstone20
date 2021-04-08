import numpy as np
import math
import matplotlib
from math import tan, cos
from threading import *
from GPS_Interface import GPS_Interface


class PathPlanning(Thread):
    GPS = GPS_Interface()
    max_velocity = 100
    max_acceleration = 100
    path_radius = 0
    seek_offset = 3
    
    def predict_location(self, current_x, current_y):
        #speed = self.GPS.get_velocity() #this method should be modified or renamed
        #bearing = self.GPS.get_relative_bearing()
        
        speed = 2.265 #this method should be modified or renamed
        bearing = 20
        sample_time = 2 # 50 is arbitrary value -> calibrate real value

        if bearing < 90:
            theta = 90 - bearing
        elif bearing < 180:
            theta = bearing - 90
        elif bearing < 270:
            theta = theta = 270 - bearing
        else:
            theta = bearing - 270

        # initial velocity vector                                                                                                 
        m = tan(math.radians(theta)) # double check
        b = current_y - m * current_x
        d = speed * sample_time
        
        future_x = cos(math.radians(90 - bearing)) * d + current_x
        future_y = future_x * m + b
        future_point = Point(future_x, future_y)
        
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


    def get_destination(self):
        destination_p = self.path.get_relative_point(self.destination_lng, self.destination_lat)
        return destination_p


    def get_location(self):
        #location_p = self.path.get_relative_point(self.GPS.get_longitude(), self.GPS.get_latitude())
        location_p = self.path.get_relative_point(2, 6)

        return location_p


    def get_normal(self,  future_p): # update for segments
        first_run = True
        shortest_dist = 0
        for segment in self.path.get_segments():
            start_p = segment.p1
            end_p = segment.p2
            m_segment = (end_p.y - start_p.y) / (end_p.x - start_p.x)

            m_normal = -1 * (1/m_segment)
            b_normal = future_p.y - m_normal * future_p.x

            x = (b_normal) / (m_segment - m_normal)
            y = m_segment * x # this will only work on original segment!

            # add check for if point is on segment
            temp_normal_point = Point(x,y)

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


    def get_correction_vector(self, current_p, normal_p, future_location, segment, velocity):
        m_segment = segment.get_slope()
        len_segment = segment.get_len()
        m_segment_normalized = m_segment / len_segment
        
        target_x = math.cos(math.atan(m_segment)) * self.seek_offset + normal_p.x
        target_y = target_x * m_segment
        target = Point(target_x, target_y)
        
        print("Target Point: " + self.print_point(target))

        # desired = Point(target_x - current_p.x, target_y - current_p.y)
        # desired.normalize()
        # desired.mult(self.max_velocity)

        # correction_vector = Point(desired.x - velocity.x, desired.y - velocity.y)
        # return correction_vector
        
        target_distance = math.sqrt((current_p.x - target.x) ** 2 + (current_p.y - target.y) ** 2)
        target_bearing = 90 - math.sin((target.y - current_p.y) / target_distance) # check

        # current velocity
        # bearing = self.GPS.get_relative_bearing()
        bearing = 20
        
        # calculate correction
        dist_future = math.sqrt((current_p.x - future_location.x) ** 2 + (current_p.y - future_location.y) ** 2)
        correction_length = math.sqrt(target_distance ** 2 + dist_future ** 2 - 2 * target_distance*dist_future * math.cos(math.radians(180 - bearing)))
        correction_bearing = math.asin((dist_future / correction_length) * math.sin(math.radians(180 - bearing))) * 180 / math.pi

        return[correction_length, correction_bearing]

    def print_point(self, p):
        x = str(p.x)
        y = str(p.y)
        return "[" + x + ", " + y + "]"

    def follow_path(self):
        dest = self.get_destination() #relative destination
        
        current_location = self.get_location()
        print("Current Location: ", self.print_point(current_location))

        # Add arival check here
        
        future_location = self.predict_location(current_location.x, current_location.y)
        print("Future Location: ", self.print_point(future_location))

        # Check if future position is within the radius of the path
        [normal_point, segment] = self.get_normal(future_location)
        print("Normal Point: ", self.print_point(normal_point))

        # distance between normal point and predicted location 
        dist = math.sqrt((future_location.x - normal_point.x) ** 2 + (future_location.y - normal_point.y) ** 2)
        
        # vehicle headed off path if dist is greater than the path radius
        if dist >= self.path_radius:
            
            correction_vector = self.get_correction_vector(current_location, normal_point, future_location, segment) 
            
            return correction_vector


    def __init__(self, lng, lat):
        Thread.__init__(self)
        self.destination_lng = lng
        self.destination_lat = lat

        # self.initial_lng = self.GPS.get_latitude()
        # self.initial_lat = self.GPS.get_longitude()
        
        self.initial_lng = 0
        self.initial_lat = 0

        self.path = Path(self.initial_lng, self.initial_lat, self.destination_lng, self.destination_lat)

        # self.follow_path()


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize():
        mag = math.sqrt((self.x) ** 2 + (self.y) ** 2)
         self.x = x / mag
         self.y = y / mag

    def mult(num):
        self.x = self.x * num
        self.y = self.y * num

    def sub(point):
        self.x = self.x - point.x
        self.y = self.y - point.y

    def add(point):
        self.x = self.x + point.x
        self.y = self.y + point.y


class Segment(): 
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def get_slope(self):
        return((self.p2.y - self.p1.y)/(self.p2.x - self.p1.x))

    def get_len(self):
        return(math.sqrt((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2))


class Path():

    def get_slope(self, desired_lng, desired_lat):
        m = (desired_lng-self.initial_lng)/(desired_lat-self.initial_lat)
        return m


    def generate_path(self, m, length): # need to add logic for segments   
        points = []
        for x in range(0, length, 100): # arbitrary sampling -> must calibrate actual value
            point = Point(x, m*x)
            points.append(point)
        return points
    

    def get_relative_point(self, lng, lat):
        #setting initial position to (0,0) all points will be measured relative to this
        rel_x = lat - self.initial_lat
        rel_y = lng - self.initial_lng
        return Point(rel_x, rel_y)


    def add_segment(self, lng, lat): 
        p = self.get_relative_point(lng, lat)
        i = 0
        for segment in self.segments:
            if p.x > segment.p1.x and p.x < segment.p2.x:
                # create and add new segment at this point
                s1 = Segment(segment.p1, p)
                s2 = Segment(p, segment.p2)

                self.segments.remove(segment)
                self.segments.insert(i, s1)
                self.segments.insert(i+1, s2)
                
                return

            i += 1

    # getters
    def get_segments(self):
        return self.segments


    def __init__(self, current_lng, current_lat, dest_lng, dest_lat):
        self.segments = []
        self.destination_lng = dest_lng
        self.destination_lat = dest_lat
        self.initial_lng = current_lng
        self.initial_lat = current_lat

        relative_destination = self.get_relative_point(self.destination_lat, self.destination_lng)
        relative_initial_point = self.get_relative_point(self.initial_lat, self.initial_lng)
        
        initial_segment = Segment(relative_initial_point, relative_destination)
        self.segments.append(initial_segment)
       
path.add_waypoint(4, 5)


path = PathPlanning(lng,lat)
correction_vector = path.follow_path()

print("Correction vector: ", target_loc)