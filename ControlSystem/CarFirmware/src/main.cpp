#define DEBUG 1 // comment out for final build

#include <Arduino.h>
#include <constants.h>
#include <io_functions.h>


char buffer[PACKET_SIZE], mt_buffer[PACKET_SIZE];
int _size;
char cmd;

bool connected = false;

motor_cmd m_cmd;
led_cmd l_cmd;

bool handshake_with_controller(){
  if(Serial.available() >= 2){
    Serial.readBytes(buffer, 2);
    return (buffer[0] == HS_1 && buffer[1] == HS_2);
  }
  return false;
}

void parse_serial_stream(){
  memcpy(buffer, mt_buffer, PACKET_SIZE);

  if(Serial.available() >= MIN_SIZE){
    cmd = Serial.read();

    switch (cmd)
    {
      case 'L':
        l_cmd.left = Serial.read() == 'T'?true:false;

      #ifdef DEBUG
        Serial.print("Left LED state: ");
        Serial.println(l_cmd.left);
      #endif

        break;

      case 'R':
        
        l_cmd.right = Serial.read() == 'T'?true:false;

      #ifdef DEBUG
        Serial.print("Right LED state: ");
        Serial.println(l_cmd.right);
      #endif

        break;

      case 'F':
        cmd = Serial.read();
        if(cmd == 'L')
          flash_left(FLASH_DURATION, NUM_FLASHES);
        else if(cmd == 'R')
          flash_right(FLASH_DURATION, NUM_FLASHES);
        else if(cmd == 'A')
          flash_all(FLASH_DURATION, NUM_FLASHES);

      #ifdef DEBUG
        Serial.print("Flashing LED: ");
        Serial.println(cmd);
      #endif
        
        break;

      case 'M':
        m_cmd.motor_speed = Serial.parseInt();
        m_cmd.motor_mode = (Serial.read() == 'T')?true:false;

      #ifdef DEBUG
        Serial.print("Executing motor command:");
        Serial.println(m_cmd.motor_speed);
      #endif

        break;

      case 'S':
        m_cmd.steering_angle = Serial.parseInt();
        m_cmd.steering_mode = true;

      #ifdef DEBUG
        Serial.print("Executing steering command:");
        Serial.println(m_cmd.steering_angle);
      #endif

        break;
      
      case 'E':
        
        connected = false;

      #ifdef DEBUG
        Serial.println("disconnecting");
      #endif
        break;

      default:
      #ifdef DEBUG
        Serial.print("cmd no work: ");
        Serial.println(cmd);
      #endif
        break;
    }

  }

}

void setup() {
  for(int i = 0 ; i < PACKET_SIZE; i++){
    buffer[i] = (char)NULL;
    mt_buffer[i] = (char)NULL;
  }

  Serial.begin(SERIAL_BAUD);
  
  pinMode(RIGHT_LED, OUTPUT);
  pinMode(LEFT_LED, OUTPUT);
  pinMode(MOTOR_FWD, OUTPUT);
  pinMode(MOTOR_REV, OUTPUT);
  pinMode(MOTOR_EN, OUTPUT);
  pinMode(STEERING_REV, OUTPUT);
  pinMode(STEERING_FWD, OUTPUT);

  l_cmd.flashing = false;
  l_cmd.left = false;
  l_cmd.right = false;

  m_cmd.motor_mode = false;
  m_cmd.motor_speed = 0;
  m_cmd.steering_angle = 0;
  m_cmd.steering_mode = false;

  flash_all(FLASH_DURATION/2, NUM_FLASHES);

#ifdef DEBUG
  Serial.println("Ready for connection");
#endif

}

void loop() {
  if(connected){
    parse_serial_stream();
    
    if(!l_cmd.flashing)
    {
      set_left_state(l_cmd.left);
      set_right_state(l_cmd.right);
    }
    else{
      if(l_cmd.left && l_cmd.right)
        flash_all(FLASH_DURATION, NUM_FLASHES);
      else if(l_cmd.right)
        flash_right(FLASH_DURATION, NUM_FLASHES);
      else if(l_cmd.left)
        flash_left(FLASH_DURATION, NUM_FLASHES);
    }
    set_motor_speed(m_cmd);
    set_steering_angle(m_cmd);
  }
  else{
    _set_motor_speed(0, false);

    delay(1000);

  #ifdef DEBUG
    Serial.println("Waiting for connection");
  #endif

    flash_all(FLASH_DURATION, NUM_FLASHES);      

    delay(500);

    set_left_state(true);
    set_right_state(true);

    if(handshake_with_controller()){
      connected = true;
      set_left_state(false);
      set_right_state(false);

    #ifdef DEBUG
      Serial.println("Connection established");
    #endif

      flash_all(FLASH_DURATION, NUM_FLASHES);      
    }
  }
}