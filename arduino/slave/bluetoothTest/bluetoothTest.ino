/*
  Example Bluetooth Serial Passthrough Sketch
 by: Jim Lindblom
 SparkFun Electronics
 date: February 26, 2013
 license: Public domain

 This example sketch converts an RN-42 bluetooth module to
 communicate at 9600 bps (from 115200), and passes any serial
 data between Serial Monitor and bluetooth module.
 */

 
#include <SoftwareSerial.h>  

int bluetoothTx = 9;  // TX-O pin of bluetooth mate
int bluetoothRx = 10;  // RX-I pin of bluetooth mate

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void setup()
{
  Serial.begin(9600); // Begin the serial monitor at 9600bps
 
 bluetooth.begin(115200); // The Bluetooth Mate defaults to 115200bps
 bluetooth.print("$"); // Print three times individually
 bluetooth.print("$");
 bluetooth.print("$"); // Enter command mode
 delay(100); // Short delay, wait for the Mate to send back CMD
 bluetooth.println("U,9600,N"); // Temporarily Change the baudrate to 9600, no parity
 // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
 bluetooth.begin(9600); // Start bluetooth serial at 9600
}

void loop()
{ 
//  TEST IF CAN SEND DATA
//  bluetooth.write("0\n");
//  bluetooth.write("1\n");
//  delay(100);
  
  if(bluetooth.available())  // If the bluetooth sent any characters
  {
    // Send any characters the bluetooth prints to the serial monitor
    Serial.println(bluetooth.parseInt());  
  }

}

