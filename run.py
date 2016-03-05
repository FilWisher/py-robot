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

  def shift(seq, n):
      n = n % len(seq)
      return seq[n:] + seq[:n]

  start_angle = 100
  rec = Recognition(False,waypoints_cw4,start_angle)
  x,y = waypoints_cw3[3]
  res = rec.sim_recognise(x,y,angle)
  print 'Expected ', (3,angle), ' got ', res
  
  waypoints = shift(waypoints_cw4,res[0]+1)
  noParticles = 100
  nav = WaypointNavigation(use_robot,waypoints,res[0],noParticles)
  nav.navigate()

