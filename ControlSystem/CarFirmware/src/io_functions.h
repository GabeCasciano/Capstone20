#include <Arduino.h>

#ifndef NAME
#include <constants.h>
#endif

typedef struct _motor_cmd_t{
  int8_t motor_speed;
  int8_t steering_angle;
  bool motor_mode, steering_mode;
}motor_cmd;

typedef struct _led_cmd_t{
    bool left, right, flashing;
}led_cmd;

void all_off(){
  digitalWrite(LEFT_LED, LOW);
  digitalWrite(RIGHT_LED, LOW);
}


void flash_left(int _dur, int _blinks){
  all_off();
  for(int i = 0; i < _blinks; i++){
    digitalWrite(LEFT_LED, HIGH);
    delay(_dur/(2*_blinks));
    digitalWrite(LEFT_LED, LOW);
    delay(_dur/(2*_blinks));
  }
}

void flash_right(int _dur, int _blinks){
  all_off();
  for(int i = 0; i < _blinks; i++){
    digitalWrite(RIGHT_LED, HIGH);
    delay(_dur/(2*_blinks));
    digitalWrite(RIGHT_LED, LOW);
    delay(_dur/(2*_blinks));
  }
}

void flash_all(int _dur, int _blinks){
    all_off();
    for(int i = 0; i < _blinks; i++){
        digitalWrite(RIGHT_LED, HIGH);
        digitalWrite(LEFT_LED, HIGH);
        delay(_dur/(2*_blinks));
        digitalWrite(RIGHT_LED, LOW);
        digitalWrite(LEFT_LED, LOW);
        delay(_dur/(2*_blinks));
    }
    all_off();
}

void set_left_state(bool _state){ digitalWrite(LEFT_LED, _state); }
void set_right_state(bool _state){ digitalWrite(RIGHT_LED, _state); }

void _set_motor_speed(int8_t _speed, bool _brake){
    uint8_t _m_out = abs(_speed) + MOTOR_OFFSET;

    if(_m_out >= MAX_MOTOR_SPEED)
        _m_out = MAX_MOTOR_SPEED;

    if(_speed > 0){
        digitalWrite(MOTOR_REV, LOW);
        analogWrite(MOTOR_FWD, _m_out);
    }
    else if(_speed < 0){
        digitalWrite(MOTOR_FWD, LOW);
        analogWrite(MOTOR_REV, _m_out);
    }
    else{
        if(_brake){
            digitalWrite(MOTOR_REV, HIGH);
            digitalWrite(MOTOR_FWD, HIGH);
        }
   
        else{
            digitalWrite(MOTOR_REV, LOW);
            digitalWrite(MOTOR_FWD, LOW);
        }
    }
}

void set_motor_speed(motor_cmd _cmd){
    if(_cmd.motor_speed != NULL)
        _set_motor_speed(_cmd.motor_speed, _cmd.motor_mode);
}



void _set_steering_angle(int8_t _angle, bool _brake){
    //if(_angle >= )

}

void set_steering_angle(motor_cmd cmd){
    _set_steering_angle(cmd.steering_angle, cmd.steering_mode);
}