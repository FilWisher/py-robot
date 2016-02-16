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
motorParams.pidParameters.k_p = 580.0
motorParams.pidParameters.k_i = 0.1
motorParams.pidParameters.k_d = 0.1

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

distance_correction = 0.45
angle_correction = 0.05

# go forwards
def forwards(cm):
    angle = cm * distance_correction
    interface.increaseMotorAngleReferences(motors, [angle, angle])

def backwards(cm):
    angle = cm * distance_correction
    interface.increaseMotorAngleReferences(motors, [-angle, -angle])

def left(degree):
    angle = degree * angle_correction
    interface.increaseMotorAngleReferences(motors, [angle, -angle])

def right(degree):
    angle = degree * angle_correction
    interface.increaseMotorAngleReferences(motors, [-angle, angle])
