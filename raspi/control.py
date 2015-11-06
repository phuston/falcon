import smbus
import time

bus = smbus.SMbus(1)

address1 = 0x04
address2 = 0x03

def writeData(address, value):
	bus.write_byte(address, value)
	return -1

def readData(address):
	value = bus.read_byte(address)
	return number

while True:
	val = raw_input("1 for on, 0 for off: ")
	add = raw_input("Which Arduino to control? 1 or 2")

	if add == 1: 
		m_address = address1
	if add == 2:
		m_address = address2

	writeData(val)
	print "RPI: Hello Arduino {}, I sent you {}".format(add, val)
	time.sleep(1)

	number = readNumber(m_address)