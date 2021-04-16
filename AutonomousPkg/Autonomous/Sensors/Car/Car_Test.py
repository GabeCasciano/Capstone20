from Autonomous.Sensors.Car.Car_Interface import Car_Interface
import time

if __name__ == "__main__":
    car = Car_Interface(loc='/dev/ttyUSB0')

    car.start()

    print("interface status", car.running)

    print("Starting Car")
    time.sleep(5)

    print("Indicating left led")
    car.left_led = True
    time.sleep(2.5)
    car.left_led = False

    time.sleep(1)

    print("Indicating right led")
    car.right_led = True
    time.sleep(2.5)
    car.right_led = False

    time.sleep(1)

    print("Flashing both lights")
    car.flash_led()
    time.sleep(3)

    for i in range(-128, 128):
        car.motor_speed = i
        time.sleep(.25)
        print("Motor speed:", i)

    for i in range(0, 128):
        car.motor_speed = 128 - i
        time.sleep(.25)
        print("Motor speed:", 128 - i)

    # speed = 125
    # print("Setting motor speed:", speed)
    # car.motor_speed = speed
    #
    # time.sleep(2.5)
    #
    # speed = 50
    # print("Setting motor speed:", speed)
    # car.motor_speed = speed
    #
    # time.sleep(2.5)
    #
    # speed = 1
    # print("Setting motor speed:", speed)
    # car.motor_speed = speed

    time.sleep(1)

    print("Exiting")
    car._exit_cmd()

    time.sleep(2)

    car.stop_thread()




