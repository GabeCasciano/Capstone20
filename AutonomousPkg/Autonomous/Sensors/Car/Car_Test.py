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
    time.sleep(5)

    car._exit_cmd()

    time.sleep(2)

    car.stop_thread()




