# Things you can run with this script:
# Without a robot:
# 1. Waypoint Navigation
# 2. Simulate recognition
# 3. Recognise location and do waypoint navigation

from canvas import *
from recognition import *

##########################
run_option = 3           #
use_robot = False        #
##########################

# 1. Waypoint Navigation
######################################################
if run_option == 1:
  initial_waypoint = 0
  noParticles = 100
  test = WaypointNavigation(use_robot,waypoints_cw3,initial_waypoint,noParticles,180)
  test.navigate()
   
# 2. Learn locations
######################################################
if run_option == 2:
  test = Recognition(False,waypoints_cw4,100)
  #test.simulateLearning()
  test.sim_testRecognition(111)

# 3. Combine the last two
######################################################  
if run_option == 3:

  # Use this function to reshuffle the waypoints depending on where you find yourself
  def shift(seq, n):
      n = n % len(seq)
      return seq[n:] + seq[:n]

  # The angle at which the robot is started
  start_angle = 100
  # The waypoint index at which the robot starts at
  waypoint_idx = 3
  x,y = waypoints_cw3[waypoint_idx]
  # Create a recognition class
  rec = Recognition(False,waypoints_cw4,start_angle)
  # Try and recognise the waypoint
  result = rec.sim_recognise(x,y,angle)
  print 'Expected ', (waypoint_idx,angle), ' got ', result
  
  # Shift the waypoints to account for the starting position
  waypoints = shift(waypoints_cw4,res[0]+1)
  # Number of particles for mcl
  noParticles = 100
  # Create a navigation class
  nav = WaypointNavigation(use_robot,waypoints,result[0],noParticles)
  # Navigate
  nav.navigate()

