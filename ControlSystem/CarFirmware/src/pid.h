#include <Arduino.h>
#include <constants.h>

typedef struct _pid_vals_t{
    int16_t input, error, output;
    int16_t accum, diff, accum_thresh;
    int16_t max_in, max_out, min_in, min_out;
}pid_vals;

void compute_pid(pid_vals *pid, int16_t target){ // FINISH
    pid->error = target - pid->input;

    pid->accum += pid->error;

    pid->output = pid->error * STR_KP;
    pid->output += (pid->diff - pid->error) * STR_KD;
    if(abs(pid->diff - pid->error) < pid->accum_thresh)
        pid->output += pid->accum * STR_KI;

    pid->output /= STR_SF;
    pid->output = map(pid->output, -MAX_STEERING_SIG + MIN_STEERING_SIG, MAX_STEERING_SIG - MIN_STEERING_SIG, MIN_STEERING_SPEED, MAX_STEERING_SPEED);

    if(abs(pid->output) > MAX_STEERING_SPEED){
        pid->output = abs(pid->output)/pid->output * MAX_STEERING_SPEED;
    }

    pid->diff = pid->error;
}