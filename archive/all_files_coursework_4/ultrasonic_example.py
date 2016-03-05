import robot
import time

port = 0 # port which ultrasoic sensor is plugged in to

robot.interface.sensorEnable(port, robot.brickpi.SensorType.SENSOR_ULTRASONIC);

while True:
	usReading = interface.getSensorValue(port)

	if usReading :
		print usReading
	else:
		print "Failed US reading"

	time.sleep(0.05)


"""
def rotate_read(start,end):
    for i in range(start,end):
        robot.right(1)
	time.sleep(1)
        print i, robot.interface.getSensorValue(port)[0]

rotate_read(0,180)
"""
interface.terminate()
