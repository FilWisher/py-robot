# CW 5: Check List
## Things we should do (not part of the script)
* Instead of shutting down by unplugging when it loses connection, we could plug in a keyboard and type 'pi\ndragonfly\nsudo reboot' or 'pi\ndragonfly\nsudo shutdown now'
##Introduction
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
* Write 'def calculate_likelihood(float x, float y, float theta, float z)', make sure it's nice and modular so we can show it to the examiner. This needs to use sonar readings and the map.
* Make sure 'def calculate_likelihood' checks the angle between the sonar and the wall is small enough to get accurate readings.
* Multiply each particle by 'calculate_likelihood' for each sonar reading.
### Normalising and Resampling (10 Marks)
* Regenerate particle set based on weights.
* This gets assessed via the whole MCL algorithm.
* Look into worsening the model to make the spreading easier to see.
### Waypoint-Based Navigation While Localising (5 marks)
* Navigate the given sequence of waypoints while doing MCL
