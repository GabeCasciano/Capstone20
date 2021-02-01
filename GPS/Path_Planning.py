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
    
    def predict_location(self, x, y):
        speed = self.GPS.get_velocity() #this method should be modified or renamed
        bearing = self.GPS.get_relative_bearing()

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
        location_p = self.path.get_relative_point(self.GPS.get_longitude(), self.GPS.get_latitude())
        return location_p

    def get_normal(self,  p): # update for segments
        shortest_dist = 10000 # arbitrary value -> change this

        for segment in self.path.get_segments():
            start_p = segment.p1
            end_p = segment.p2
            m = (end_p.y - start_p.y) / (end_p.x - start_p.x)
            m_normal = -1 * (1/m)
            b_normal = p.y - m_normal * p.x

            x = (b_normal) / (m - m_normal)
            y = m * x

            temp_normal_point = Point(x,y)

            # need segment will shortest normal point
            dist = math.sqrt((p.x - normal_point.x) ** 2 + (p.y - normal_point.y) ** 2)
            if dist < shortest_dist:
                normal_point = temp_normal_point


        return normal_point

    def is_on_path(self, p):
        # start_point = Point(0,0)
        # end_point = self.get_destination()
        normal_point = self.get_normal(p)

        dist = math.sqrt((p.x - normal_point.x) ** 2 + (p.y - normal_point.y) ** 2)

        return dist < self.path_radius

    def seek(self, target, velocity): #implement
        return

    def follow_path(self):
        target_offset = 50
        dest = self.get_destination()
        current_location = self.get_location()
        future_location = self.predict_location(current_location.x, current_location.y)

        # Check if future position is within the radius of the path
        normal_point = self.get_normal(future_location)
        
        #on_path = self.is_on_path(future_location)

        # distance between normal point and predicted location 
        dist = math.sqrt((future_location.x - normal_point.x) ** 2 + (future_location.y - normal_point.y) ** 2)
        
        # vehicle headed off path if dist is greater than the path radius
        if dist >= self.path_radius:
            target_location = Point(normal_point.x + target_offset, normal_point.y) #fix this math
            self.seek(target_location, self.max_velocity)


    def __init__(self, lng, lat):
        self.destination_lng = lng
        self.destination_lat = lat

        self.initial_lng = self.GPS.get_latitude()
        self.initial_lat = self.GPS.get_longitude()

        self.path = Path(lng, lat)

        self.follow_path()


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Segment(): # still need to implement adding new segments
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


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

    def __init__(self, lng, lat):
        self.segments = []
        self.destination_lng = lng
        self.destination_lat = lat
        self.initial_lng = self.GPS.get_latitude()
        self.initial_lat = self.GPS.get_longitude()

        relative_destination = self.get_relative_point(self.destination_lng, self.destination_lat)
        relative_initial_point = self.get_relative_point(self.initial_lng, self.initial_lat)
        
        initial_segment = Segment(relative_initial_point, relative_destination)
        self.segments.append(initial_segment)
       
       # generate points along path -> will probably remove this
        m = self.get_slope(lng, lat)
        d = self.GPS.get_distance_to([lng, lat])
        self.points = self.generate_path(m, d)


p = Path(1,40)
