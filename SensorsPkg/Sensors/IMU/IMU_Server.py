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

    def pack_and_send(self, command:int, data, addr):
        out = str(command) + ","
        if type(data) is list:
            for i in range(0, len(data)):
                out += str(data[i]) + ","
        else:
            out += str(data)
        self.socket.sendto(str.encode(out), addr)

    def run(self) -> None:
        self.imu.start()
        print("Beginning IMU data server on port: " + str(self.port))
        self.socket.bind(('',self.port))
        while self.running:
            message, addr = self.socket.recvfrom(1024)
            data = message.decode().split(",")
            # format data string
            if '' in data:
                data.remove('')
            data = [int(data[i], 16) for i in range(0, len(data))]

            if data[0] == 0x1: # get the lin accel
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_linear_acceleration(data[1])
                else:
                    data = self.imu.get_linear_acceleration()
                
                self.pack_and_send(1, data, addr)

            elif data[0] == 0x2: # get the angular pos
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_angular_orientation(data[1])
                else:
                    data = self.imu.get_angular_orientation()

                self.pack_and_send(2, data, addr)

            elif data[0] == 0x3: # get the angular velocity
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_angular_velocity(data[1])
                else:
                    data = self.imu.get_angular_velocity()

                self.pack_and_send(3, data, addr)

            elif data[0] == 0x4: # get sample rate 
                if len(data) > 1 and data[1] < 3:
                    data = self.imu.get_sample_rate(data[1])
                else:
                    data = self.imu.get_sample_rate()

                self.pack_and_send(4, data, addr)

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
            
            elif data[0] == 0x66:
                temp = "ack"
                self.socket.sendto(str.encode(temp), addr)
        self.socket.close()

    def stop_thread(self):
        self.running = False
    
    def exit_handler(self):
        self.imu.stop_thread()
        print("Stopping IMU data server")

if __name__ == "__main__":
    Server = IMU_Server()
    atexit.register(Server.exit_handler)
    Server.start()
    # sock = socket(AF_INET, SOCK_DGRAM)
    # sock.sendto(str.encode("1"), ("localhost", 8001))
    # msg, addr = sock.recvfrom(1024)
    # print(msg.decode())
