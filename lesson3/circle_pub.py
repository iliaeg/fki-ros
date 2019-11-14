#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Подключаем библиотеку для работы с ROS
import rospy
# Импортируем обьект для работы с движением
from geometry_msgs.msg import Twist

rospy.init_node('go_circle')
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(1)

vel_msg = Twist()
vel_msg.linear.x = 0.16
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 2.0

def stop():
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0

def go_circle(time):
    global vel_msg, velocity_publisher
    t0 = rospy.Time.now().to_sec()
    t1 = t0
    velocity_publisher.publish(vel_msg)
    while not rospy.is_shutdown():#(t1 - t0) <= time:
        print rospy.Time.now()
        # print 't0 = ',t0, ' t1 = ',t1
        t1 = rospy.Time.now().to_sec()
        # print 'moving'
        velocity_publisher.publish(vel_msg)
        # rate.sleep()

    stop()
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    print '__main__'
    go_circle(10) # for 10 seconds