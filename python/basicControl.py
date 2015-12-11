import serial
import time

baud_rt = 57600
port0 = '/dev/rfcomm0'
# port1 = '/dev/rfcomm2'
# port2 = '/dev/rfcomm3'
ser_timeout = 50

raw_input( "Press ENTER to begin bluetooth serial connection...")

# try:
ser0 = serial.Serial(port0,baud_rt,timeout=ser_timeout)
# time.sleep(.5)
# ser1 = serial.Serial(port1,baud_rt,timeout=ser_timeout)
# time.sleep(.5)
# ser2 = serial.Serial(port2,baud_rt,timeout=ser_timeout)


# except:
# 	print "Error"


while True:
	data = raw_input()
	ser0.write(data)
	# ser1.write(data)
	# ser2.write(data)

