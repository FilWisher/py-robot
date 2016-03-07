#!/usr/bin/env python

import brickpi
import sys
import time

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
    RADS_PDG = 0.0348
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

        motorParams = self.interface.MotorAngleControllerParameters()
        motorParams.maxRotationAcceleration = self.speed
        motorParams.maxRotationSpeed = self.acceleration
        motorParams.feedForwardGain = 255/20.0
        motorParams.minPWM = 18.0
        motorParams.pidParameters.minOutput = -255
        motorParams.pidParameters.maxOutput = 255
        motorParams.pidParameters.k_p = self.kp
        motorParams.pidParameters.k_i = self.ki
        motorParams.pidParameters.k_d = self.kd

        self.interface.setMotorAngleControllerParameters(motors[0], motorParams)
        self.interface.setMotorAngleControllerParameters(motors[1], motorParams)
        # self.interface.setMotorAngleControllerParameters(motors[2], motorParams)

        return motors

    def setup_sonar(self):
        self.interface.sensorEnable(self.port, brickpi.SensorType.SENSOR_ULTRASONIC)
    """
        HELPER Functions
    """

    # Motor Related
    def validateMove(self):
        while not self.interface.motorAngleReferencesReached(self.motors):
            time.sleep(0.1)

    def get_angles(self):
        angles = self.interface.getMotorAngles(self.motors)
        return angles[0][0], angles[1][0]

    def startLogging(self, logfile):
        self.interface.startLogging(logfile)

    def stopLogging(self):
        self.interface.stopLogging()

    # Sonar Related
    def getSensorMeasurement(self):
        # 18 is distance of sensor from center of rotation
        time.sleep(0.1)
    	return self.interface.getSensorValue(self.port)
   
    def measure360(self):
        rads = self.RADS_PDG*360/20
        
        for i in range(0,20):
            self.interface.increaseMotorAngleReferences(self.motors, [-rads, rads])
            while not self.interface.motorAngleReferenceReached(self.motors):
                print self.getSensorMeasurement()
                time.sleep(0.1)

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
            r.measure360()
        elif (sys.argv[1] == 'z'):
            print "hey"
            print r.getSensorMeasurement()
        else:
            print_usage()
    except:
        print_usage()
