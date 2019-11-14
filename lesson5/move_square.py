#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
# Подключаем библиотеку для работы с ROS
import rospy
# Импортируем обьект для работы с нужными нам сообщениями
from nav_msgs.msg import Odometry
# Импортируем обьект для работы с движением
from geometry_msgs.msg import Twist, Point

rospy.init_node('move_square_node', anonymous=True)

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

rate = rospy.Rate(1)
rate_odom = rospy.Rate(20000)

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
        print "--- init_state ---"
        print "start_x = ", start_x
        print "start_y = ", start_y
        print "start_angle = ", start_angle
        print "------------------"

    def init_xy(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        print "--- init_xy ---"
        print "start_x = ", start_x
        print "start_y = ", start_y
        print "------------------"

    def init_theta(self, start_angle):
        self.start_angle = start_angle
        print "--- init_theta ---"
        print "start_angle = ", start_angle
        print "------------------"

robot = RobotState(False, 0.0, 0.0, False, 0.0, False)

class Pose:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

def go_forward():
    global robot
    global vel_msg
    vel_msg.linear.x = 0.1
    robot.forward = True

def stop_forward():
    global robot
    global vel_msg
    vel_msg.linear.x = 0.0
    robot.forward = False

def go_turn():
    global robot
    global vel_msg
    vel_msg.angular.z = 0.6
    robot.turn = True

def stop_turn():
    global robot
    global vel_msg
    vel_msg.angular.z = 0.0
    robot.turn = False

def distance(x, y, x_start, y_start):
    return math.sqrt( (x-x_start)**2 + (y-y_start)**2 )

# # from tf.transformations import *

# # # Преобразование из Эйлера в кватернион
# # quaternion = quaternion_from_euler(0, 0, 0)

# # # Преобразование из кватерниона в углы Эйлера
# # euler = euler_from_quaternion(quaternion)

# class to store pose
pose = Pose(0, 0, 0)

#distance to go forward in meters
s = 0.3

counter = 0

finish = False
cycle = False

velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def update_pose(data):
    """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
    # # rostopic echo /odom
    # print "X = ",  msg.pose.pose.position.x
    # print "Y = ",  msg.pose.pose.position.y
    # print "theta = ", quaternion_to_theta(msg.pose.pose.orientation)
    global counter, velocity_publisher
    print "=== callback function === ", counter
    counter += 1
    global robot, pose, cycle
    pose.x = data.pose.pose.position.x
    pose.y = data.pose.pose.position.y
    pose.theta = quaternion_to_theta(data.pose.pose.orientation) + 180
    if cycle:
        pose.theta += 360
    if not robot.is_init:
        robot.init_state(pose.x, pose.y, pose.theta)
        robot.is_init = True
    global s
    if robot.forward:
        dist = distance(pose.x, pose.y, robot.start_x, robot.start_y)
        # print "x = ", pose.x, " y = ", pose.y
        # print "distance = ", dist
        if dist >= s:
            stop_forward()
            velocity_publisher.publish(vel_msg)

            robot.init_theta(pose.theta)
            go_turn()
            velocity_publisher.publish(vel_msg)
    if robot.turn:
        if pose.theta > 357 and pose.theta < 360:
            cycle = True
        cur_angle = abs(pose.theta - robot.start_angle)
        # print "pose.theta = ", pose.theta
        # print "cur_angle = ", cur_angle
        if cur_angle > 84.5 and cur_angle <= 91.0:
            stop_turn()
            velocity_publisher.publish(vel_msg)

            robot.turn_counter += 1
            if robot.turn_counter == 4:
                exit(0)
            
            robot.init_xy(pose.x, pose.y)
            go_forward()
            velocity_publisher.publish(vel_msg)

    # rate_odom.sleep()

    # print "X = ", pose.x #," ", round(pose.x, 4)
    # print "robot X = ", robot.start_x
    # print "Y = ", pose.y #," ", round(pose.y, 4)
    # print "robot Y = ", robot.start_y

    # print "theta = ", pose.theta
    # print "robot theta = ", robot.start_angle



def move():
    print "Hello Im robot"

    global velocity_publisher
    t0 = rospy.Time.now().to_sec()
    t1 = rospy.Time.now().to_sec()
    pose_subscriber = rospy.Subscriber('/odom', Odometry, update_pose)
    go_forward())

    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rate.sleep()
        pass

if __name__ == '__main__':
    # try:
    # #Testing our function
    move()
    # except rospy.ROSInterruptException: pass