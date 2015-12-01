#include <SoftwareSerial.h>  

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

int bluetoothTx = 9;  // TX-O pin of bluetooth mate
int bluetoothRx = 10;  // RX-I pin of bluetooth mate

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void setup() {
  Serial.begin(9600);
  pinMode(pinAm1, OUTPUT);
  pinMode(pinBm1, OUTPUT);
  pinMode(pinEnm1, OUTPUT);

  pinMode(pinAm2, OUTPUT);
  pinMode(pinBm2, OUTPUT);
  pinMode(pinEnm2, OUTPUT);

  digitalWrite(pinEnm1, HIGH);

  bluetooth.begin(115200); // The Bluetooth Mate defaults to 115200bps
  bluetooth.print("$"); // Print three times individually
  bluetooth.print("$");
  bluetooth.print("$"); // Enter command mode
  delay(100); // Short delay, wait for the Mate to send back CMD
  bluetooth.println("U,9600,N"); // Temporarily Change the baudrate to 9600, no parity
  // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
  bluetooth.begin(9600); // Start bluetooth serial at 9600
}

void loop() {
  
  // BLUETOOTH CONFIGURATION
  if(bluetooth.available() > 0)  // If the bluetooth sent any characters
  {
    // Send any characters the bluetooth prints to the serial monitor
    in = bluetooth.parseInt();
     Serial.println(in);  
  }

  //  WIRED SERIAL CONNECTION
//  if (Serial.available() > 0) {
//    in = Serial.parseInt();
//  }

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
