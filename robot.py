# go forwards
def forwards(cm):
    angle = cm * 0.45
    interface.increaseMotorAngleReferences(motors, [angle, angle])

def backwards(cm):
    angle = cm * 0.45
    interface.increaseMotorAngleReferences(motors, [-angle, -angle])
    
def left(degree):
    angle = cm * 0.17
    interface.increaseMotorAngleReferences(motors, [angle, -angle])
    
def right(degree):
    angle = cm * 0.17
    interface.increaseMotorAngleReferences(motors, [-angle, angle])
