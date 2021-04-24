from Autonomous.Sensors.Car.Car_Interface import Car_Interface
import time

if __name__ == "__main__":
    car = Car_Interface(loc='/dev/ttyUSB1')

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

    car.steering_angle = 0;

    for i in range(-128, 128):
        car.motor_speed = i
        time.sleep(.25)
        print("Motor speed:", i)

    car.motor_speed = 0

    for i in range(-30, 30):
        car.steering_angle = i
        time.sleep(.25)
        print("steer angle", i)

    for i in range(-30, 30):
        car.steering_angle = 60 - i
        time.sleep(.25)
        print("steer angle:", 60 - i)

    car.steering_angle = 0;

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




