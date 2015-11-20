import serial
import time

baud_rt = 9600
port1 = '/dev/rfcomm0'
ser_timeout = 50

raw_input( "Press ENTER to begin bluetooth serial connection...")

try:
	ser = serial.Serial(port1,baud_rt,timeout=ser_timeout)
except:
	print "Error"


while True:
	data = raw_input()
	ser.write(data)