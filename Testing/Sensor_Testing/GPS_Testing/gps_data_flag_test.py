import unittest
from Sensors.GPS.GPS_Interface import GPS_Interface
from time import sleep


gps_ser_loc = "/dev/ttyACM0"
gps_ser_baud = 4800

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.gps = GPS_Interface(gps_ser_loc, gps_ser_baud)  # Set up the GPS interface
        self.gps.start()  # Start the gps thread
        sleep(5)  # wait for a sec to let the thread start and collect some initial data

    def tearDown(self) -> None:
        self.gps.stop_thread()  # Stop the
        self.gps.join()

    def test_gps_data_flag(self):
        for i in range(0, 10):  # give the GPS an opportunity to try
            if self.gps.get_position() == [0.0, 0.0]:  # If the gps does not have a fix aka 0,0
                self.assertEqual(self.gps.get_new_data_flag(), False)  # the new data flag should be false
                sleep(2)  # wait 2 second and try again
            else:
                self.assertEqual(self.gps.get_new_data_flag(), True)  # if the flag is set test algo works, otw its not working probably
                break  # break out


if __name__ == '__main__':
    unittest.main()
