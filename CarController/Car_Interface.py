from threading import *
from socket import *
import sys


class Car_Interface(Thread):

    _MAX_STEERING_ANGLE = 100
    _MIN_STEERING_ANGLE = 0
    _MID_STEERING_ANGLE = 50

    _MAX_CAR_SPEED = 255
    _MIN_CAR_SPEED = -255

    def __init__(self, addr: str = "10.10.1.2", port: int = 8080):
        super(Car_Interface, self).__init__()

        self._car_addr = addr
        self._car_port = port

        self._car_sock = socket(AF_INET, SOCK_DGRAM)

        self.__req_steering_angle = 0  # expecting values between -180 and 180
        self.__req_car_speed = 0  # expecting values between -255 and 255
        self.__up_counter = 0 # used for watch dog

        self.__car_battery = 0
        self.__car_code = 0
        self.__car_steering_angle = 0
        self.__car_speed = 0

        self.running = True
        self._stopped = False

    def _gen_packet(self, pack_type:int = 0, data_req: int = 0) -> bytes:
        data = []
        if pack_type == 0: # motor commands
            data.append(pack_type)
            data.append(self.__req_car_speed)
            data.append(self.__req_steering_angle)

        elif pack_type == 1: # data commands
            # 0 full system info (batt, error_code, steering_angle, car_speed)
            # 1 system health (batt, error_code)
            # 2 battery level
            # 3 steering_angle
            # 4 car_speed
            if data_req in range(0, 4): # 5 being max possible command number
                data.append(pack_type)
                data.append(data_req)

        elif pack_type == 2: # stop command
            data.append(pack_type)

        # adds a counter value on the end of each packet to provide a metric for the car to make sure we haven't
        # timedout
        if data.__len__() > 0:
            data.append(self.__up_counter)
            self.__up_counter += 1
            if self.__up_counter >= 2 ** 8:
                self.__up_counter = 0

        return bytes(data)

    def _send_motor_speed(self):
        if not self._stopped:
            data = self._gen_packet()
            self._car_sock.sendto(data, (self._car_addr, self._car_port))

    def _send_stop(self):
        self._stopped = True
        data = self._gen_packet(2)
        self._car_sock.sendto(data, (self._car_addr, self._car_port))

    def _send_data_req(self, data:int = 0):
        if data in range(0, 4):
            _data = self._gen_packet(1, data)
            self._car_sock.sendto(_data, (self._car_addr, self._car_port))

    def _get_data_req(self):
        data, addr = self._car_sock.recvfrom(128)
        data = list(data)

        if data.__len__() >= 1:
            self._parse_data_req(data)

    def _parse_data_req(self, data: list):
        if data[0] == 0:
            self.__car_battery = int(data[1])
            self.__car_code = int(data[2])
            self.__car_steering_angle = int(data[3])
            self.__car_speed = int(data[4])
        elif data[0] == 1:
            self.__car_battery = int(data[1])
            self.__car_code = int(data[2])
        elif data[0] == 2:
            self.__car_battery = int(data[1])
        elif data[0] == 3:
            self.__car_steering_angle = int(data[1])
        elif data[0] == 4:
            self.__car_speed = int(data[1])

    # properties
    @property
    def speed(self) -> int:
        return self.__req_car_speed

    @speed.setter
    def speed(self, value: int):
        if Car_Interface._MAX_CAR_SPEED >= value >= Car_Interface._MIN_CAR_SPEED:
            self.__car_speed = value

    @property
    def steering_angle(self) -> int:
        return self.__req_steering_angle

    @steering_angle.setter
    def steering_angle(self, value: int):
        if Car_Interface._MAX_STEERING_ANGLE >= value >= Car_Interface._MIN_STEERING_ANGLE:
            self.__req_steering_angle = value

    @property
    def battery_level(self) -> int:
        return self.__car_battery

    def error_code(self) -> int:
        return self.__car_code
    # thread functions
    def start(self) -> None:
        super(Car_Interface, self).start()
        self.running = True

    def run(self) -> None:
        self._send_data_req(0)
        while self.running:
            # for every 5 motor commands sent send 1 data query
            # run until stopped, constantly outputting
            for i in range(0, 4):
                self._send_motor_speed()
            self._send_data_req(0)
            self._get_data_req()