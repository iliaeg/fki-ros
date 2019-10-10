#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
# Подключаем библиотеку для работы с ROS
import rospy
# Импортируем обьект для работы с нужными нам сообщениями
from nav_msgs.msg import Odometry
# Импортируем обьект для работы с движением
from geometry_msgs.msg import Twist, Point

def quaternion_to_theta(orientation):

    t1 = +2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
    t2 = +1.0 - 2.0 * (orientation.y ** 2 + orientation.z**2)

    return math.degrees(math.atan2(t1, t2))

angle = 0
Point position = 0

def get_angle(odom_data):
    # rostopic echo /odom
    global angle
    angle =  quaternion_to_theta(odom_data.pose.pose.orientation)
    global position
    position = odom_data.pose.pose.position

# # from tf.transformations import *

# # # Преобразование из Эйлера в кватернион
# # quaternion = quaternion_from_euler(0, 0, 0)

# # # Преобразование из кватерниона в углы Эйлера
# # euler = euler_from_quaternion(quaternion)

# # Простая функция "каллбек". Данная функция вызываеться
# # в момент когда появились данные. В нашем примере
# # выводи данные на экран
# def callback(msg):
#     # rostopic echo /odom
#     print "X = ",  msg.pose.pose.position.x
#     print "Y = ",  msg.pose.pose.position.y
#     print "theta = ", quaternion_to_theta(msg.pose.pose.orientation)

# # Инициализируем ноду ROS
# rospy.init_node('temp_odom_subscr_1')
# # Создаем подписчиака, в параметрах указываем
# # Название топика, тип сообщения, имя функцим каллбека
# sub = rospy.Subscriber('odom', Odometry, callback)
# # Выводим информационное сообщение
# # print sub.header

# rospy.loginfo("I am a odom_subscriber_1")
# # # Передаем у
# rospy.spin()

def get_angle_wrapper():
    # make node
    # rospy.init_node('ilia_odometry', anonymous=True)
    sub = rospy.Subscriber('odom', Odometry, get_angle)

def move():
    # Starts a new node
    # rospy.init_node('robot_turtle_node_1', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_forward_msg = Twist()

    print("Let's move your robot")
    # Set variable to move forward with speed x
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
    vel_turn_msg.angular.z = 1.2

    # while not rospy.is_shutdown():

    #distance to go forward in meters
    s = 0.2

    for i in range(4):
        ### Move s meters forward
        # Setting the current time
        t0 = rospy.Time.now().to_sec()
        t1 = t0

        while (t1-t0)*vel_forward_msg.linear.x < s:
            #Publish the velocity
            velocity_publisher.publish(vel_forward_msg)
            #Takes actual time
            t1 = rospy.Time.now().to_sec()

        ### Make 90-degree turn
        # Setting the current angle
        get_angle_wrapper()
        d0 = angle
        d1 = d0

        while (abs(d1-d0)) < 90.0:
            #Publish the velocity
            velocity_publisher.publish(vel_turn_msg)
            #Takes actual angle
            get_angle_wrapper()
            d1 = angle
            # print "d0 = ", d0
            # print "d1 = ", d1
            print "abs = ", abs(d1-d0)

    #After the loop, stops the robot
    vel_forward_msg.linear.x = 0
    #Force the robot to stop
    velocity_publisher.publish(vel_forward_msg)

# def begin():
#     while not rospy.is_shutdown():
#         # make node
#         rospy.init_node('ilia_odometry', anonymous=True)
#         sub = rospy.Subscriber('odom', Odometry, move)

if __name__ == '__main__':
    try:
        # begin()
        # make node
        rospy.init_node('ilia_odometry', anonymous=True)
        # sub = rospy.Subscriber('odom', Odometry, move)
        # #Testing our function
        move()
    except rospy.ROSInterruptException: pass