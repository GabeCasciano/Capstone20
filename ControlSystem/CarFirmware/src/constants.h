#define NAME "CarFirmware"
#define VERSION "1.0.0"

#define RIGHT_LED 2
#define LEFT_LED 3
#define STEERING_REV 6
#define STEERING_FWD 7
#define MOTOR_EN 8 // active low
#define MOTOR_REV 9
#define MOTOR_FWD 10

#define STEERING_IN A6

// Serial constants 

#define SERIAL_BAUD 9600

#define PACKET_SIZE 64
#define MIN_SIZE 2

#define HS_1 'G'
#define HS_2 'c'

#define TERMINATOR ';'

// Motor constants
#define MOTOR_OFFSET 0
#define MAX_MOTOR_SPEED 255
#define MIN_MOTOR_SPEED 50

// Steering constants
#define MAX_STEERING_ANGLE 30
#define MAX_STEERING_SIG 775
#define MIN_STEERING_ANGLE -30
#define MIN_STEERING_SIG 300
#define MIN_STEERING_SPEED -255
#define MAX_STEERING_SPEED 255
#define STR_SPEED 100
#define STEERING_OFFSET 30
#define STR_KP 1
#define STR_KD 1
#define STR_KI 1
#define STR_SF 5

// Led constants
#define FLASH_DURATION 2000
#define NUM_FLASHES 4