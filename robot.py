import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]
speed = 6.0

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 12.0
motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 400.0
motorParams.pidParameters.k_i = 0.1
motorParams.pidParameters.k_d = 0.1

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

distance_correction = 0.362
angle_correction = 0.05
motor_smoothing = 1.0

# Ultrasonic sensor
port = 0 # port which ultrasoic sensor is plugged in to
interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC)

# go forwards
def forwards(cm):
    angle = cm * distance_correction
    move(angle*0.9999,angle)

def backwards(cm):
    angle = cm * distance_correction
    move(-angle,-angle)

def left(degree):
    angle = degree * angle_correction
    move(angle,-angle)

def right(degree):
    angle = degree * angle_correction
    move(-angle,angle)

def get_angles():
    motorAngles = interface.getMotorAngles(motors)
    a1 = motorAngles[0][0]
    a2 = motorAngles[1][0]
    return a1,a2

def move(delta_a1,delta_a2):
    #delta_a2 corresponds to the left motor
    delta_a1 *= motor_smoothing
    initial_a1, initial_a2 = get_angles()
    target_a1 = initial_a1 + delta_a1
    target_a2 = initial_a2 + delta_a2
    interface.increaseMotorAngleReferences(motors, [delta_a1, delta_a2])

    dif1t1 = 0
    dif2t1 = 0
    while(True):
        a1,a2 = get_angles()
        """
        dif1 = (target_a1-a1)
        dif2 = (target_a2-a2)
        """
        dif1t2 = (target_a1-a1)
        dif2t2 = (target_a2-a2)
	#print dif1t1, dif2t1
        #print dif1t2, dif2t2
	#print
        #if(abs(dif1) + abs(dif2) < 0.25):
        if( dif1t1 == dif1t2 and dif2t1 == dif2t2):
            break
        time.sleep(0.3)
        dif1t1 = (target_a1-a1)
        dif2t1 = (target_a2-a2)

def getSensorMeasurement():
	usReading = interface.getSensorValue(port)
	time.sleep(0.1)
    # 18 is distance of sensor from center of rotation
	return usReading[0] + 18


#function to draw a square
def square(cm):

    forwards(cm)
    right(90)
    forwards(cm)
    right(90)
    forwards(cm)
    right(90)
    forwards(cm)
    right(90)
