#include <Arduino.h>
#include <constants.h>
#include <pid.h>

typedef struct _motor_cmd_t{
  int8_t motor_speed;
  int8_t steering_angle;
  bool motor_mode, steering_mode;
}motor_cmd;

typedef struct _led_cmd_t{
    bool left, right, flashing;
}led_cmd;

pid_vals steering_pid;

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

    if(_speed > 1){
        digitalWrite(MOTOR_REV, LOW);
        analogWrite(MOTOR_FWD, _m_out);
    }
    else if(_speed < -1){
        digitalWrite(MOTOR_FWD, LOW);
        analogWrite(MOTOR_REV, _m_out);
    }
    else{
        analogWrite(MOTOR_REV, 1);
        analogWrite(MOTOR_FWD, 1);
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

void init_pid(){
    steering_pid.max_in = MAX_STEERING_SIG * STR_SF;
    steering_pid.max_out = MAX_STEERING_SPEED;
    steering_pid.min_in = MIN_STEERING_SIG * STR_SF;
    steering_pid.min_out = MIN_MOTOR_SPEED;
}

void _set_steering_angle(int8_t _angle, bool _brake){
    int temp = map(_angle, MIN_STEERING_ANGLE, MAX_STEERING_ANGLE, MIN_STEERING_SIG, MAX_STEERING_SIG);
    int val = temp - analogRead(STEERING_IN) ;
    
    if(val > 5){
        digitalWrite(STEERING_REV, LOW);
        analogWrite(STEERING_FWD, 128 - STR_SPEED);
        Serial.print("fwd");
    }
    else if(val < -5){
        digitalWrite(STEERING_FWD, LOW);
        analogWrite(STEERING_REV, 128 - STR_SPEED);
        Serial.print("rev");
    }
    else{
        analogWrite(STEERING_REV, 1);
        analogWrite(STEERING_FWD, 1);

        if(_brake){
            digitalWrite(STEERING_FWD, HIGH);
            digitalWrite(STEERING_REV, HIGH);
        }else{
            digitalWrite(STEERING_FWD, LOW);
            digitalWrite(STEERING_REV, LOW);
        }
    }
    Serial.print("diff");
    Serial.println(val);
}

void set_steering_angle(motor_cmd cmd){
    _set_steering_angle(cmd.steering_angle, cmd.steering_mode);
}
