//
// Created by Misha on 9/7/2019.
//

#include "SmoothServo.h"
#include <Arduino.h>

SmoothServo::SmoothServo(int speed, int init) {
    this->speed = speed;
    this->goal = init;
    this->pos = init;
}

void SmoothServo::init(Servo *servo) {
    this->servo = servo;
    this->servo->writeMicroseconds(pos);
    this->l_time = millis();
}

SmoothServo::~SmoothServo() = default;

void SmoothServo::write(int goal) {
    this->goal = goal;
}

int SmoothServo::togo() {
    return goal - pos;
}

int SmoothServo::read() {
    return this->pos;
}

void SmoothServo::run() {
    unsigned long time = millis();
    unsigned long delta = time - l_time;
    if (delta < (unsigned) (1000 / speed)) return;

    if (pos != goal) {
        pos += (goal - pos < 0 ? -1 : 1) * min((int) delta * speed / 1000, abs(goal - pos));
        servo->writeMicroseconds(pos);
    }

    l_time = time;
}