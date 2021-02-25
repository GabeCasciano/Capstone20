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
    path_radius = 20
    seek_offset = 20
    
    def predict_location(self, x, y):
        #speed = self.GPS.get_velocity() #this method should be modified or renamed
        #bearing = self.GPS.get_relative_bearing()
        
        speed = 44 #this method should be modified or renamed
        bearing = 23

        # initial velocity vector
        m = tan(90 - bearing) 
        b = y - m * x
        d = speed * 50 # 50 is arbitrary value -> calibrate real value
        
        future_x = cos(90 - bearing) * d
        future_y = future_x * m + b
        future_point = Point(future_x, future_y)
        
        return future_point
    
    
    def add_waypoint(self, lng, lat): #implement as part of segmentation
        return 0


    def get_destination(self):
        destination_p = self.path.get_relative_point(self.destination_lng, self.destination_lat)
        return destination_p


    def get_location(self):
        #location_p = self.path.get_relative_point(self.GPS.get_longitude(), self.GPS.get_latitude())
        location_p = self.path.get_relative_point(699, 2345)

        return location_p


    def get_normal(self,  p): # update for segments
        first_run = True
        for segment in self.path.get_segments():
            start_p = segment.p1
            end_p = segment.p2
            m_segment = (end_p.y - start_p.y) / (end_p.x - start_p.x)
            m_normal = -1 * (1/m_segment)
            b_normal = p.y - m_normal * p.x

            x = (b_normal) / (m_segment - m_normal)
            y = m_segment * x

            temp_normal_point = Point(x,y)

            # need segment with shortest normal distance
            dist = math.sqrt((p.x - temp_normal_point.x) ** 2 + (p.y - temp_normal_point.y) ** 2)
            if first_run:
                normal_point = temp_normal_point
                closest_segment = segment
                shortest_dist = dist 
                first_run = False
            if dist < shortest_dist:
                normal_point = temp_normal_point
                closest_segment = segment
                shortest_dist = dist
        
        return [normal_point, closest_segment]


    def get_correction_vector(self, current_p, normal_p, future_location, segment):
        m_segment = segment.get_slope()
        len_segment = segment.get_len()
        m_segment_normalized = m_segment / len_segment

        target_x = normal_p.x + self.seek_offset * m_segment_normalized
        target_y = normal_p.y + self.seek_offset * m_segment_normalized
        target = Point(target_x, target_y)

        target_distance = math.sqrt((current_p.x - target.x) ** 2 + (current_p.y - target.y) ** 2)
        target_bearing = 90 - math.sin((target.y - current_p.y) / target_distance)

        # current velocity
        # bearing = self.GPS.get_relative_bearing()
        bearing = 133
        
        # calculate correction
        dist_future = math.sqrt((current_p.x - future_location.x) ** 2 + (current_p.y - future_location.y) ** 2)
        correction_length = math.sqrt(target_distance ** 2 + dist_future ** 2 - 2 * target_distance*dist_future * math.cos(180 - bearing))
        correction_bearing = math.sinh((dist_future / target_distance) * math.sin(180 - bearing))

        return[correction_length, correction_bearing]


    def follow_path(self):
        dest = self.get_destination() #relative destination
        current_location = self.get_location()
        future_location = self.predict_location(current_location.x, current_location.y)

        # Check if future position is within the radius of the path
        [normal_point, segment] = self.get_normal(future_location)
        
        # distance between normal point and predicted location 
        dist = math.sqrt((future_location.x - normal_point.x) ** 2 + (future_location.y - normal_point.y) ** 2)
        
        # vehicle headed off path if dist is greater than the path radius
        if dist >= self.path_radius:
            
            target_location = self.get_correction_vector(current_location, future_location, normal_point, segment) 
            
            return target_location


    def __init__(self, lng, lat):
        Thread.__init__(self)
        self.destination_lng = lng
        self.destination_lat = lat

        # self.initial_lng = self.GPS.get_latitude()
        # self.initial_lat = self.GPS.get_longitude()
        
        self.initial_lng = 2345
        self.initial_lat = 2333

        self.path = Path(self.initial_lng, self.initial_lat, self.destination_lng, self.destination_lat)

        # self.follow_path()


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment(): 
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def get_slope(self):
        return((self.p2.y - self.p1.y)/(self.p2.x - self.p1.x))

    def get_len(self):
        return(math.sqrt((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2))


class Path():
    GPS = GPS_Interface()

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


    def add_segment(self, p): # not complete
        for segment in self.segments:
            if p.x > segment.p1.x and p.x < segment.p2.x:
                # create and add new segment at this point
                return


    # getters
    def get_segments(self):
        return self.segments


    def __init__(self, current_lng, current_lat, dest_lng, dest_lat):
        self.segments = []
        self.destination_lng = dest_lng
        self.destination_lat = dest_lat
        self.initial_lng = current_lng
        self.initial_lat = current_lat

        relative_destination = self.get_relative_point(self.destination_lng, self.destination_lat)
        relative_initial_point = self.get_relative_point(self.initial_lng, self.initial_lat)
        
        initial_segment = Segment(relative_initial_point, relative_destination)
        self.segments.append(initial_segment)
       
       # generate points along path -> will probably remove this
        # m = self.get_slope(dest_lng, dest_lat)
        # d = self.GPS.get_distance_to([dest_lng, dest_lat])
        # self.points = self.generate_path(m, d)

path = PathPlanning(20,40)
target_loc = path.follow_path()
print(target_loc)