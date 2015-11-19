int pinAm1 = 2;
int pinBm1 = 3;
int pinEnm1 = 4;

int pinAm2 = 5;
int pinBm2 = 6;
int pinEnm2 = 7;

int led = 13;
char in;
int steps = 226;
int dir;
int dis;
int len;
int moveM;


void setup() {
  Serial.begin(9600);
  pinMode(pinAm1, OUTPUT);
  pinMode(pinBm1, OUTPUT);
  pinMode(pinEnm1, OUTPUT);

  pinMode(pinAm2, OUTPUT);
  pinMode(pinBm2, OUTPUT);
  pinMode(pinEnm2, OUTPUT);

  digitalWrite(pinEnm1, HIGH);
}

void loop() {

  if (Serial.available() > 0) {
    in = Serial.parseInt();
  }

  if (in < 0) {
    dir = 0;
    dis = round(in*(-.01)*steps);
    digitalWrite(led, HIGH);
  }

  else {
    dir = 1;
    dis = round(in*.01*steps);
    // Serial.println(in*steps);
  }

  len = (int) dis;
  pulse(dis, dir, 1);

  // if(in == 1) {
  //   Serial.print('1');
  //   pulse(steps, 1, 1);
  //   delay(100);
  // }

  // if(in == -1) {
  //   pulse(steps, 0, 1);
  //   delay(100);
  // }

delay(100);
  in = 0;
}

void pulse(int steps, int direction, int speed) {
  digitalWrite(pinAm1, direction);
  if (speed == 0) {
    digitalWrite(pinEnm1, LOW);
    delay(50);
    digitalWrite(pinEnm1, HIGH);
  }
  for (int i = 0; i < steps; i=i+1) {
    digitalWrite(pinBm1, HIGH);
    delayMicroseconds(10);
    digitalWrite(pinBm1, LOW);
  }
}
