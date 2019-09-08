#include <Arduino.h>
#include <Servo.h>
#include "SmoothServo.h"

static const int SERVO_PIN_THETA = 5;
static const int SERVO_PIN_PHI = 6;
static const int SERVO_PIN_FOCUS = 9;
static const int TRIG_PIN = 3;
static const int ECHO_PIN = 4;

Servo servoTheta, servoPhi, servoFocus;
SmoothServo smoothServoTheta(300, 1500);
SmoothServo smoothServoPhi(300, 1500);

double distCm();

bool readyDist();

int asc(const void *c1, const void *c2);

int radToMicro(double rad);

static unsigned long lastMeas;

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    lastMeas = millis();

    servoTheta.attach(SERVO_PIN_THETA);
    servoPhi.attach(SERVO_PIN_PHI);
    servoFocus.attach(SERVO_PIN_FOCUS);

    smoothServoTheta.init(&servoTheta);
    smoothServoPhi.init(&servoPhi);
}

void loop() {

    if (readyDist()) {
        double x = distCm();
        double a = -0.01685393258;
        double b = 17.887640449;
        servoFocus.write((int) ((x * a + b) * 10.0));
    }


    smoothServoTheta.run();
    smoothServoPhi.run();
}

#define N 20

double distCm() {
    double values[N];

    for (int i = 0; i < N; i++) {
        lastMeas = millis();
        digitalWrite(TRIG_PIN, LOW);
        delayMicroseconds(5);
        digitalWrite(TRIG_PIN, HIGH);
        delayMicroseconds(10);
        digitalWrite(TRIG_PIN, LOW);

        pinMode(ECHO_PIN, INPUT);
        values[i] = (pulseIn(ECHO_PIN, HIGH) / 2.0) / 29.1;
    }

    qsort((void *) values, N, sizeof(double), (int (*)(const void *, const void *)) (asc));
    lastMeas = millis();

    return values[N - 1];
}

bool readyDist() {
    return millis() - lastMeas > 500;
}

int asc(const void *c1, const void *c2) {
    double a = *((double *) c1);
    double b = *((double *) c2);

    return a > b ? 1 : (a < b ? -1 : 0);
}

int radToMicro(double rad) {
    return max(min(1500 + (int) (1000.0 * rad / PI), 1800), 1200);
}
