import serial
import io

if __name__ == "__main__":
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 115200

    ser.open()
    data_word = [0x50, 0x03, 0x00, 0x3d, 0x00, 0x03, 0x00, 0x00]

    print(bytes(data_word))
    #ser.write(data_word)
    going = True
    while going:
        temp = ser.read(1)
        val = hex(int.from_bytes(temp,byteorder='little'))
        print(val)

    ser.close()