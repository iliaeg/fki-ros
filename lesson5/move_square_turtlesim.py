#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
# Подключаем библиотеку для работы с ROS
import rospy
# Импортируем обьект для работы с нужными нам сообщениями
from nav_msgs.msg import Odometry
# Импортируем обьект для работы с движением
from geometry_msgs.msg import Twist, Point
from turtlesim.msg import Pose

def quaternion_to_theta(orientation):

    t1 = +2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
    t2 = +1.0 - 2.0 * (orientation.y ** 2 + orientation.z**2)

    return math.degrees(math.atan2(t1, t2))

vel_msg = Twist()
vel_msg.linear.x = 0
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 0

class RobotState:
    def __init__(self, forward, start_x, start_y, turn, start_angle, is_init):
        self.forward = forward
        self.forward_counter = 0
        self.start_x = start_x
        self.start_y = start_y
        self.turn = turn
        self.turn_counter = 0
        self.start_angle = start_angle
        self.is_init = is_init

    def init_state(self, start_x, start_y, start_angle):
        self.start_x = start_x
        self.start_y = start_y
        self.start_angle = start_angle

robot = RobotState(False, 0.0, 0.0, False, 0.0, False)

def go_forward():
    global robot
    global vel_msg
    vel_msg.linear.x = 0.2
    robot.forward = True

def stop_forward():
    global robot
    global vel_msg
    vel_msg.linear.x = 0.0
    robot.forward = False

def go_turn():
    global robot
    global vel_msg
    vel_msg.angular.z = 0.9
    robot.turn = True

def stop_turn():
    global robot
    global vel_msg
    vel_msg.angular.z = 0.0
    robot.turn = False

def distance(x, y, x_start, y_start):
    return math.sqrt( (x-x_start)**2 + (y-y_start)**2 )

# A subscriber to the topic '/turtle1/pose'. self.update_pose is called
# when a message of type Pose is received.
pose = Pose()

#distance to go forward in meters
s = 1

def update_pose(data):
    """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
    global robot
    pose = data
    pose.theta = pose.theta * 180 / math.pi
    if not robot.is_init:
        robot.init_state(pose.x, pose.y, pose.theta)
        robot.is_init = True
    global s
    if robot.forward:
        if distance(pose.x, pose.y, robot.start_x, robot.start_y) >= s:
            stop_forward()
            robot.forward_counter += 1
            # robot.init_state(pose.x, pose.y, pose.theta)
            robot.is_init = False
            go_turn()
    if robot.turn:
        if abs(pose.theta - robot.start_angle) >= 90:
            stop_turn()
            robot.turn_counter += 1
            if robot.turn_counter == 4:
                exit(0)
            # robot.init_state(pose.x, pose.y, pose.theta)
            robot.is_init = False
            go_forward()

    print "X = ", pose.x #," ", round(pose.x, 4)
    print "robot X = ", robot.start_x
    print "Y = ", pose.y #," ", round(pose.y, 4)
    print "robot Y = ", robot.start_y
    print "theta = ", pose.theta
    print "robot theta = ", robot.start_angle

pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, update_pose)

def move():
    # Starts a new node
    # rospy.init_node('robot_turtle_node_1', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    go_forward()
    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        # make node
        rospy.init_node('ilia_odometry', anonymous=True)
        # sub = rospy.Subscriber('odom', Odometry, move)
        move()
    except rospy.ROSInterruptException: pass