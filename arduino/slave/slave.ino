#include <Wire.h>

#define SLAVE_ADDRESS 0x04


void setup() {
	pinmode(13, OUTPUT);

	Wire.begin(SLAVE_ADDRESS);

	//Define callbacks for I2C communication
	Wire.onReceive(receivedData);
	Wire.onRequest(sendData);

	Serial.println("Ready!");
}

void loop(){
	//Nothing to do here yet
}

//Callback for received data
void receiveData(int byteCount){

	while(Wire.available()) {
		number 
	}
}