#!/usr/bin/env python

import brickpi
import sys
import time
import numpy as np
import os
import math

class Robot(object):

    """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        EDIT the parameters below to calibrate the robot
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    """
    # Motor Movement correction. Radians per centimeter
    RADS_PCM = 0.541
    # Motor Rotation correction. Radians per degree
    RADS_PDG = 0.0517
    # Sonar Rotation correction.
    SONAR_RADS_PDG = 0.027

    # SENSOR port
    port = 3

    # Wheel adjustments
    LEFT_WHEEL = 1.0
    RIGHT_WHEEL = 0.991

    # Robot speed
    acceleration = 6.0
    speed = 12.0

    # Robot PCI
    kp = 180
    ki = 360
    kd = 30

    """
        END OF ROBOT PARAMETERS
    """

    # Initialized in init
    interface = []
    motors = []
    motorParams = []

    # Robot init and exit
    def __init__(self):
        self.interface = brickpi.Interface()
        self.interface.initialize()

        self.motors = self.setup_motors()
        self.setup_sonar()

    def __exit__(self, type, value, traceback):
        self.interface.terminate()

    def setup_motors(self):
        motors = [1, 0]

        self.interface.motorEnable(motors[0])
        self.interface.motorEnable(motors[1])
        # self.interface.motorEnable(motors[2])

        self.motorParams = self.interface.MotorAngleControllerParameters()
        self.motorParams.maxRotationAcceleration = self.acceleration
        self.motorParams.maxRotationSpeed = self.speed
        self.motorParams.feedForwardGain = 255/20.0
        self.motorParams.minPWM = 18.0
        self.motorParams.pidParameters.minOutput = -255
        self.motorParams.pidParameters.maxOutput = 255
        self.motorParams.pidParameters.k_p = self.kp
        self.motorParams.pidParameters.k_i = self.ki
        self.motorParams.pidParameters.k_d = self.kd

        self.interface.setMotorAngleControllerParameters(motors[0], self.motorParams)
        self.interface.setMotorAngleControllerParameters(motors[1], self.motorParams)
        # self.interface.setMotorAngleControllerParameters(motors[2], motorParams)

        return motors

    def setup_sonar(self):
        self.interface.sensorEnable(self.port, brickpi.SensorType.SENSOR_ULTRASONIC)
    """
        HELPER Functions
    """

    # Motor Related

    def changeSpeed(self, accel, veloc):
        self.motorParams.maxRotationAcceleration = accel
        self.motorParams.maxRotationSpeed = veloc

        self.interface.setMotorAngleControllerParameters(self.motors[0], self.motorParams)
        self.interface.setMotorAngleControllerParameters(self.motors[1], self.motorParams)

    def resetSpeed(self):
        self.motorParams.maxRotationAcceleration = self.acceleration
        self.motorParams.maxRotationSpeed = self.speed

        self.interface.setMotorAngleControllerParameters(self.motors[0], self.motorParams)
        self.interface.setMotorAngleControllerParameters(self.motors[1], self.motorParams)

    def validateMove(self):
        while not self.interface.motorAngleReferencesReached(self.motors):
            time.sleep(0.1)

    def getAngles(self):
        angles = self.interface.getMotorAngles(self.motors)
        return angles[0][0], angles[1][0]

    def startLogging(self, logfile):
        self.interface.startLogging(logfile)

    def stopLogging(self):
        self.interface.stopLogging()

    # Sonar Related
    def getSensorMeasurement(self):
        # 18 is distance of sensor from center of rotation
        time.sleep(0.01)
    	return self.interface.getSensorValue(self.port)[0]

    def _resampleData(self,angles,readings):
        if(len(angles) != len(readings)):
            print 'ERROR resampleData a different amount of readings and angles.'
        numberOfBins=360
        data = np.zeros(numberOfBins)
        count = np.zeros(numberOfBins)

        for i in range(len(angles)):
            index = int(round(angles[i])) % 360
            data[index] += float(readings[i])
            count[index] += 1

        for i in range(numberOfBins):
            if(count[i] != 0):
                data[i] /= float(count[i])

        return data.astype(int).tolist()

    def measure360(self):
        self.changeSpeed(1.0, 2.0)
        print 'ouiahsfioahnfs'
        rads = self.RADS_PDG*360
        l0,r0 = self.getAngles()

        self.interface.increaseMotorAngleReferences(self.motors, [-rads, rads])
        angles = []
        readings = []

        while not self.interface.motorAngleReferencesReached(self.motors):
            lc,rc = self.getAngles()
            angles.append((abs(lc-l0) + abs(rc-r0))/(2.0*self.RADS_PDG))
            readings.append(self.getSensorMeasurement())

        print len(angles)
        self.validateMove()
        self.resetSpeed()

        return self._resampleData(angles,readings)

    """
       Movement functions
    """
    def move(self, distance):
        rads = self.RADS_PCM * distance

        self.interface.increaseMotorAngleReferences(self.motors, [rads*self.LEFT_WHEEL, rads*self.RIGHT_WHEEL])
        self.validateMove()

    def turn(self, angle):
        rads = self.RADS_PDG * angle

        self.interface.increaseMotorAngleReferences(self.motors, [-rads, rads])
        self.validateMove()

    # Movement by name
    def forwards(self, cm):
        self.move(cm)

    def backwards(self, cm):
        self.move(-cm)

    def left(self, degree):
        self.turn(degree)

    def right(self, degree):
        self.turn(-degree)

    #function to draw a square
    def square(self, cm):
        self.forwards(cm)
        self.right(90)
        self.forwards(cm)
        self.right(90)
        self.forwards(cm)
        self.right(90)
        self.forwards(cm)
        self.right(90)

if __name__ == "__main__":
    def print_usage():
        print "== USAGE =="
        print "r angle (in degrees)"
        print "m distance (in cm)"

    r = Robot()

    try:
        if (sys.argv[1] == 't'):
            r.turn(float(sys.argv[2]))
        elif (sys.argv[1] == 'm'):
            r.move(float(sys.argv[2]))
        elif (sys.argv[1] == 'f'):
            r.forwards(float(sys.argv[2]))
        elif (sys.argv[1] == 'b'):
            r.backwards(float(sys.argv[2]))
        elif (sys.argv[1] == 'l'):
            r.left(float(sys.argv[2]))
        elif (sys.argv[1] == 'r'):
            r.right(float(sys.argv[2]))
        elif (sys.argv[1] == 's'):
            print "hey"
            print r.measure360()
        elif (sys.argv[1] == 'z'):
            print "hey"
            print r.getSensorMeasurement()
        else:
            print_usage()
    except:
        print_usage()
