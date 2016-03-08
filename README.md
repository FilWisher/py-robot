# robot
uncertain robot on brickpi which can navigate waypoints in its sleep

### File structure
* `archive/` - needs sorting
* `canvas.py` - draws on the canvas and defines the walls of the environment
* `navigation.py` - navigates a robot through the environment using particles class
* `particles.py` - defines a particle class which supports MCL localisation
* `recognition.py` - can learn and recognise waypoints by doing a sonar sweep
* `robot.py` - control for robot motors and sensors
* `run.py` - example use cases
