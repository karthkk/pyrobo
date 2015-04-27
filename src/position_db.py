"""
Maintains a database of angles to actual end effector position.  This db is used to make minor adjustments to the inverse kinematcs solution.
 This is needed as the robot position is also affected by inaccuracies in the initial configs of servos and tolerances in servo performance
"""

