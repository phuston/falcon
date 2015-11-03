int pinA = 2;
int pinB = 3;
int pinEn = 4;

void setup() {
  Serial.begin(9600);
  pinMode(pinA, OUTPUT);
  pinMode(pinB, OUTPUT);
  pinMode(pinEn, OUTPUT);
}

void loop() {
  Serial.begin(9600);
  digitalWrite(pinEn, HIGH);
  pulse(800, 1, 1);
  delay(1000);
  pulse(1600, 0, 0);
  delay(1000);
}

void pulse(int steps, int direction, int speed) {
  digitalWrite(pinA, direction);
  if (speed == 0) {
    digitalWrite(pinEn, LOW);
    delay(100);
    digitalWrite(pinEn, HIGH);
  }
  for (int i = 0; i < steps; i=i+1) {
    digitalWrite(pinB, HIGH);
    delayMicroseconds(10);
    digitalWrite(pinB, LOW);
  }
}
