#include <Arduino.h>
#include <Servo.h>

static const int SERVO_PIN_THETA = 5;
static const int SERVO_PIN_PHI = 6;
static const int SERVO_PIN_FOCUS = 9;
static const int TRIG_PIN = 3;
static const int ECHO_PIN = 4;
static const int INC = 2;
static const int WAIT = 100 * INC;

Servo servoTheta, servoPhi, servoFocus;

double distCm();

bool readyDist();

int asc(const void *c1, const void *c2);

static unsigned long lastMeas;
static double r, dr, r_new;
static int theta, phi;

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    lastMeas = millis();

    servoTheta.attach(SERVO_PIN_THETA);
    servoPhi.attach(SERVO_PIN_PHI);
    servoFocus.attach(SERVO_PIN_FOCUS);

    theta = 90;
    phi = 75;

    servoTheta.write(theta);
    servoPhi.write(phi);
    delay(500);
    r = distCm();
}

void loop() {
    dr = -1.0;
    // Theta
    while (dr < 0) {
        theta -= max((int) (INC * fmin(fabs(dr), 3.0)), INC);
        servoTheta.write(theta);
        delay(WAIT);

        r_new = distCm();
        dr = r_new - r;
        r = r_new;
        Serial.println(theta);
    }

    dr = -1.0;
    while (dr < 0) {
        theta += max((int) (INC * fmin(fabs(dr), 3.0)), INC);
        servoTheta.write(theta);
        delay(WAIT);

        r_new = distCm();
        dr = r_new - r;
        r = r_new;
        Serial.println(theta);
    }

//    dr = -1.0;
//    // Phi
//    while (dr < 0) {
//        phi -= max((int) (INC * fmin(fabs(dr), 3.0)), INC);
//        servoPhi.write(phi);
//        delay(WAIT);
//
//        r_new = distCm();
//        dr = r_new - r;
//        r = r_new;
//        Serial.println(phi);
//    }
//
//    dr = -1.0;
//    while (dr < 0) {
//        phi += max((int) (INC * fmin(fabs(dr), 3.0)), INC);
//        servoPhi.write(phi);
//        delay(WAIT);
//
//        r_new = distCm();
//        dr = r_new - r;
//        r = r_new;
//        Serial.println(phi);
//    }

    // Focus
    if (readyDist()) {
        double x = distCm();
        lastMeas = millis();
        double a = -0.01685393258;
        double b = 17.887640449;
        servoFocus.write((int) ((x * a + b) * 10.0));
    }
}

#define N 25

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
        values[i] = (pulseIn(ECHO_PIN, HIGH, 12066) / 2.0) / 29.1;

        if (values[i] <= 0.0) i--;
    }

    qsort((void *) values, N, sizeof(double), (int (*)(const void *, const void *)) (asc));


    return values[N / 2];
}

bool readyDist() {
    return millis() - lastMeas > 500;
}

int asc(const void *c1, const void *c2) {
    double a = *((double *) c1);
    double b = *((double *) c2);

    return a > b ? 1 : (a < b ? -1 : 0);
}
