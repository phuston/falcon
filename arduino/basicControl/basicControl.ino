int pinAm1 = 2;
int pinBm1 = 3;
int pinEnm1 = 4;

int pinAm2 = 5;
int pinBm2 = 6;
int pinEnm2 = 7;


void setup() {
  Serial.begin(9600);
  pinMode(pinAm1, OUTPUT);
  pinMode(pinBm1, OUTPUT);
  pinMode(pinEnm1, OUTPUT);

  pinMode(pinAm2, OUTPUT);
  pinMode(pinBm2, OUTPUT);
  pinMode(pinEnm2, OUTPUT);
}

void loop() {

  pulse(800, 1, 0);
  delay(2000);
}

void pulse(int steps, int direction, int speed) {
  digitalWrite(pinAm1, direction);
  if (speed == 0) {
    digitalWrite(pinEnm1, LOW);
    delay(100);
    digitalWrite(pinEnm1, HIGH);
  }
  for (int i = 0; i < steps; i=i+1) {
    digitalWrite(pinBm1, HIGH);
    delayMicroseconds(10);
    digitalWrite(pinBm1, LOW);
  }
}
