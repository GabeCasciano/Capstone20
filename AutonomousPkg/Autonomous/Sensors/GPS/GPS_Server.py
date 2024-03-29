from socket import *
from Sensors.GPS.GPS_Interface import *
from threading import *
import atexit

class GPS_Server(Thread):

    def __init__(self, loc: str = '/dev/ttyACM0', baud:int = 4800, port:int=8002):
        self.gps = GPS_Interface(loc, baud)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port = port
        self.running = True

        super(GPS_Server, self).__init__()

    def pack_and_send(self, command: int, data, addr):
        out = str(command) + ","
        if type(data) is list:
            for i in range(0, len(data)):
                out += str(data[i]) + ","
        else:
            out += str(data)
        self.socket.sendto(str.encode(out), addr)

    def run(self) -> None:
        self.gps.start()
        print("Beginning GPS data server on port:" + str(self.port))
        self.socket.bind(('', self.port))

        while self.running:
            message, addr = self.socket.recvfrom(1024)
            data = message.split(",")

            # format data string
            if len(data) > 1:
                lat = float(data[1])
                lon = float(data[2])

            data[0] = int(data[0], 16)

            if data[0] == 0x1: # get position
                data = self.gps.position
                self.pack_and_send(0x1, data, addr)

            elif data[0] == 0x2: # get lat
                data = self.gps.latitude
                self.pack_and_send(0x2, data, addr)

            elif data[0] == 0x3: # get long
                data = self.gps.longitude
                self.pack_and_send(0x3, data, addr)

            elif data[0] == 0x7: # get ground speed
                data = self.gps.ground_speed
                self.pack_and_send(0x7, data, addr)

            elif data[0] == 0x8: # get sample rate
                data = self.gps.sample_rate
                self.pack_and_send(0x8, data, addr)

        self.socket.close()

    def stop_thread(self):
        self.running = False
    
    def exit_handler(self):
        self.gps.stop_thread()
        print("Stopping GPS data server")

if __name__ == "__main__":
    Server = GPS_Server()
    atexit.register(Server.exit_handler)
    Server.start()