from socket import *
from IMU_Interface import *
from threading import *
import atexit

class IMU_Server(Thread):

    def __init__(self, loc:str = '/dev/ttyUSB0', baud:int=115200, port:int=8001):
        self.imu = IMU_Interface(loc, baud)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port = port
        self.running = True

        super(IMU_Server, self).__init__()

    
    def run(self) -> None:
        print("Beginning IMU data server on port: " + str(self.port))
        self.socket.bind(('',self.port))

        while self.running:
            message, addr = self.socket.recvfrom(1024)
            data = message.split(",")
        
            # format data string
            if '' in data:
                data.remove('')
            data = [int(data[i], 16) for i in range(0, len(data))]

            if data[0] == 0x1: # get the lin accel
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_linear_acceleration(data[1])
                else:
                    data = self.imu.get_linear_acceleration()
                
                self.socket.sendto(str(data), addr)

            elif data[0] == 0x2: # get the angular pos
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_angular_orientation(data[1])
                else:
                    data = self.imu.get_angular_orientation()

                self.socket.sendto(str(data), addr)

            elif data[0] == 0x3: # get the angular velocity
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_angular_velocity(data[1])
                else:
                    data = self.imu.get_angular_velocity()

                self.socket.sendto(str(data), addr)

            elif data[0] == 0x4: # get sample rate 
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_sample_rate(data[1])
                else:
                    data = self.imu.get_sample_rate()

                self.socket.sendto(str(data), addr)

            elif data[0] == 0x5: # zero lin accel
                self.imu.zero_lin_accel()
            elif data[0] == 0x6: # zero angular pos
                self.imu.zero_rel_angular_pos()
            elif data[0] == 0x7: # zero angular vel
                self.imu.zero_angular_vel()
            elif data[0] == 0x8: # zero relatives
                self.imu.zero_rel_lin_accel()
                self.imu.zero_rel_angular_pos()
                self.imu.zero_rel_angular_vel()

    def stop_thread(self):
        self.running = False
    
    def exit_handler(self):
        self.imu.stop_thread()
        print("Stopping IMU data server")

if __name__ == "__main__":
    Server = IMU_Server()
    atexit.register(Server.exit_handler)
    Server.start()
