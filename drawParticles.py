import random
import numpy as np
import time
import robot

c = 0;
sigmaX = sigmaY = 1.6
sigmaT = 0.2

def getRandomX():
    return random.gauss(0,sigmaX)

def getRandomY():
    return random.gauss(0,sigmaY)

def getRandomTheta():
    return random.gauss(0,sigmaT)

numberOfParticles = 100

#initialise particles
particles = [(100,100,0) for i in range(numberOfParticles)]
particleHistory = []
print "drawParticles:" + str(particles)


def Mean(listOfTuples):
    xSum = 0
    ySum = 0
    thetaSum = 0
    numberOfTuples = len(listOfTuples)
    for t in listOfTuples:
        x, y, theta = t
        xSum += x
        ySum += y
        thetaSum += theta

    return (xSum/numberOfTuples, ySum/numberOfTuples, thetaSum/numberOfTuples)

#function to move particles straight
def moveParticles(cm):
        initialPosition = Mean(particles)
        #update particle position after moving cm distance
        for i in range(numberOfParticles):
                x,y,theta = particles[i]
                e = getRandomX()
                f = getRandomTheta()


                particles[i] = ((x + (cm + e)*np.cos(np.deg2rad(theta))), (y + (cm + e)*np.sin(np.deg2rad(theta))), (theta + f))
                nx,ny,ntheta = particles[i]
        newPosition = Mean(particles)
        line = (initialPosition[0], initialPosition[1], newPosition[0], newPosition[1])
        print "drawLine:" + str(line)



#function to rotate particles deg degrees
def rotateParticles(deg):

        #update particle position after moving cm distance
        for i in range(numberOfParticles):
                x,y,theta = particles[i]

                f = getRandomTheta()

                particles[i] = (x, y, theta + deg + f)


#function to draw a square
def drawSquare(cm):
        scaling_factor = 10
        for i in range(4):
            for j in xrange(4):
                robot.forwards(cm/4)
                time.sleep(0.1)
                moveParticles(cm*scaling_factor/4)
                saveParticles()
                print "drawParticles:" + str(particleHistory)
            robot.left(90)
            rotateParticles(90)

def saveParticles():
    for p in particles:
        particleHistory.append(p)

drawSquare(40)
