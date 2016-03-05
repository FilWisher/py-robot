# CW 5: Check List

##Introduction
The following is an attempt to condense the spec.
* This practical only needs sonar and wheels.
* Due Friday 26th
* Robot should be able to move around the mapped environment in small steps of 20cm, pausing after each movement.
* After motion, the robot should make a sonar measurement of the distance of the wall in front and use this to adjust the particle weights based on a likelihood function.
*  Then, it should normalise and resample the particle distribution and be ready to complete another motion step.
*  By repeating these steps the robot will be able to keep track of its location accurately.
* Code for displaying the map http://www.doc.ic.ac.uk/˜ajd/Robotics/RoboticsResources/particleDataStructures.py.
* Define the centre of rotation as (0,0)
* The sonar should be mounted horizontally and at a height ideally
above 10cm and below 25cm to be sure that it ‘sees’ all the walls of the environment
* The sonar is not at (0,0) so calculate a correction.

## Objectives

###  Sonar Likelihood and Measurement Update (10 Marks)
* Write `calculate_likelihood(float x, float y, float theta, float z)`, make sure it's nice and modular so we can show it to the examiner. This needs to use sonar readings and the map.
* Make sure `calculate_likelihood` checks the angle between the sonar and the wall is small enough to get accurate readings.
* Multiply each particle by 'calculate_likelihood' for each sonar reading.

### Normalising and Resampling (10 Marks)
* After having weighted each particle with `calculate_likelihood` regenerate the particles proportional to their weight.
* This gets assessed via the whole MCL algorithm.
* Look into worsening the uncertainty to make the spreading easier to see and hence assess.

### Waypoint-Based Navigation While Localising (5 marks)
* Navigate the given sequence of waypoints while doing MCL.

## Miscellaneous things to do for next week
* Split up the tasks/make a plan.
* Don't erase the particle cloud at each movement
* Change the line we draw to be the ideal line, not just the trajectory of particle 0.
* Instead of shutting down by unplugging the battery when it loses connection, we could plug in a keyboard and type `pi, PASSWORD, sudo reboot` or `pi, PASSWORD, sudo shutdown now`
* Reorganise the code somewhat, maybe use classes?
* Maybe start printing to a log file so we can debug the sensors and motors?
