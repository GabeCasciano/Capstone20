from Autonomous.Sensors.Car.Car_Interface import Car_Interface
import time

if __name__ == "__main__":
    car = Car_Interface()

    car.start()

    print("Starting Car")
    time.sleep(1)

    print("Indicating left led blink")
    car.left_led = True
    time.sleep(2.5)

    print("Indicating right led blink")
    car.right_led = True
    time.sleep(2.5)




