#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist

def move():
    # Starts a new node
    rospy.init_node('robot_cleaner_1', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_forward_msg = Twist()

    print("Let's move your robot")
    # Set variable to move forward with speed = 0.1
    vel_forward_msg.linear.x = 0.1
    vel_forward_msg.linear.y = 0
    vel_forward_msg.linear.z = 0
    vel_forward_msg.angular.x = 0
    vel_forward_msg.angular.y = 0
    vel_forward_msg.angular.z = 0

    vel_turn_msg = Twist()
    # Set variable to make U-turn
    vel_turn_msg.linear.x = 0
    vel_turn_msg.linear.y = 0
    vel_turn_msg.linear.z = 0
    vel_turn_msg.angular.x = 0
    vel_turn_msg.angular.y = 0
    vel_turn_msg.angular.z = 1.57

    # while not rospy.is_shutdown():

    for i in range(2):
        ### Move 10s forward
        # Setting the current time
        t0 = rospy.Time.now().to_sec()
        t1 = rospy.Time.now().to_sec()

        while (t1-t0) < 10:
            #Publish the velocity
            velocity_publisher.publish(vel_forward_msg)
            #Takes actual time
            t1 = rospy.Time.now().to_sec()

        ### Make U-turn
        # Turn 1,57 rad/s during 2s => 180 degree turn
        # Setting the current time
        t0 = rospy.Time.now().to_sec()
        t1 = rospy.Time.now().to_sec()

        while (t1-t0) < 2:
            #Publish the velocity
            velocity_publisher.publish(vel_turn_msg)
            #Takes actual time
            t1 = rospy.Time.now().to_sec()

    #After the loop, stops the robot
    vel_forward_msg.linear.x = 0
    #Force the robot to stop
    velocity_publisher.publish(vel_forward_msg)

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass