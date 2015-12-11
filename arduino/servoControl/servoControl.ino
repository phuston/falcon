#include <SoftwareSerial.h>

int pinAm1 = 2;
int pinBm1 = 3;
int pinEnm1 = 4;

int led = 13;
char in;
int steps = 226;
int dir;
int dis;
int len;
int moveM;
int pulseDelay;

int bluetoothTx = 9;  // TX-O pin of bluetooth mate
int bluetoothRx = 10;  // RX-I pin of bluetooth mate

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void setup() {
  Serial.begin(9600);
  pinMode(pinAm1, OUTPUT);
  pinMode(pinBm1, OUTPUT);
  pinMode(pinEnm1, OUTPUT);

  digitalWrite(pinEnm1, HIGH);

//  bluetooth.begin(115200); // The Bluetooth Mate defaults to 115200bps
//  bluetooth.print("$"); // Print three times individually
//  bluetooth.print("$");
//  bluetooth.print("$"); // Enter command mode
//  delay(100); // Short delay, wait for the Mate to send back CMD
//  bluetooth.println("U,19.2,N"); // Temporarily Change the baudrate to 9600, no parity
//  // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
  bluetooth.begin(57600); // Start bluetooth serial at 9600
}

void loop() {

  // BLUETOOTH CONFIGURATION
  if(bluetooth.available() > 0)  // If the bluetooth sent any characters
  {
//    Serial.println(bluetooth.parseInt());;
    // Send any characters the bluetooth prints to the serial monitor
    in = bluetooth.parseInt();
    Serial.println(in);  
  }

//  //  WIRED SERIAL CONNECTION
//  if (Serial.available() > 0) {
//    in = Serial.parseInt();
//    Serial.println(in);
//  }
  
  if (in < 0) {
    dir = 0;
    dis = round(in*(-.01)*steps);
  }
  
  else {
    dir = 1;
    dis = round(in*.01*steps);
  }
  
  // len = (int) dis;
  if (dis == 0) {
    delayMicroseconds(2660);
  }
  pulse(dis, dir, 1);
  
  delay(100);
    in = 0;
}


void pulse(int steps, int direction, int speed) {

  pulseDelay = 2660/steps;

  digitalWrite(pinAm1, direction);
  if (speed == 0) {
    digitalWrite(pinEnm1, LOW);
    delay(50);
    digitalWrite(pinEnm1, HIGH);

  }
  for (int i = 0; i < steps; i=i+1) {
    digitalWrite(pinBm1, HIGH);
    delayMicroseconds(pulseDelay);
    digitalWrite(pinBm1, LOW);
  }
}