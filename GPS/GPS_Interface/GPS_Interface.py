from serial import Serial
from serial import tools
from threading import *

class GPS(Thread):

    data_queue = []
    NMEA_VALID_COMMANDS = ["GPGLL", "GPRMC", "GPTRF", "GPVBW", "GPVTG"]

    def __init__(self, loc: str, baud: int):
        self.gps_serial = Serial(loc, baud)
        self.latitude = 0
        self.longitude = 0
        self.ground_speed = 0
        self.bearing_true = 0
        self.bearing_magnetic = 0
        self.how_valid = 0

        self.relative_latitude = 0
        self.relative_longitude = 0

        self.running = True

        if not self.gps_serial.isOpen():
            self.gps_serial.open()

        self.gps_worker = self.worker(self.gps_serial)

    # --- Parsing thread ---

    def run(self) -> None:
        while self.running:
            data = str.split(self.ser.readline().__str__(), ",")
            command = data.pop()

            if command is "GPGGA":
                self.parse_GGA(data)
            elif command is "GPGLL":
                self.parse_GGL(data)
            elif command is "GPRMC":
                self.parse_RMC(data)
            elif command is "GPTRF":
                self.parse_TRF(data)
            elif command is "GPVBW":
                self.parse_VBW(data)

    # --- Parsing functions ---

    def parse_GGA(self, data: str):
        pass

    def parse_GGL(self, data: str):
        pass

    def parse_RMC(self, data: str):
        pass

    def parse_TRF(self, data: str):
        pass

    def parse_VBW(self, data: str):
        pass

    def parse_VTG(self, data: str):
        pass

    # --- Get Data functions ---

    def get_velocity(self) -> float:
        pass

    def get_bearing_true(self) -> float:
        pass

    def get_bearing_magnetic(self) -> float:
        pass

    def get_position(self) -> list:
        pass

    def zero_location(self):
        pass

    def get_relative_distance(self) -> list:
        pass

    def get_distance_to(self, goal: list) -> list:
        pass




