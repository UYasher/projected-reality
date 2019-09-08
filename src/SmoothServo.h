//
// Created by Misha on 9/7/2019.
//

#ifndef PROJECTED_REALITY_SMOOTHSERVO_H
#define PROJECTED_REALITY_SMOOTHSERVO_H

#include <Servo.h>

class SmoothServo {
public:
    explicit SmoothServo(int speed, int init);

    ~SmoothServo();

    void init(Servo *servo);

    void write(int goal);

    int read();

    int togo();

    void run();

private:
    Servo *servo;
    int pos, goal;
    int speed; // degrees/ 1000ms
    unsigned long l_time;
};


#endif //PROJECTED_REALITY_SMOOTHSERVO_H
