#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
# Подключаем библиотеку для работы с ROS
import rospy
# Импортируем обьект для работы с нужными нам сообщениями
from nav_msgs.msg import Odometry

def quaternion_to_theta(orientation):

    t1 = +2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
    t2 = +1.0 - 2.0 * (orientation.y ** 2 + orientation.z**2)

    return math.degrees(math.atan2(t1, t2))

# from tf.transformations import *

# # Преобразование из Эйлера в кватернион
# quaternion = quaternion_from_euler(0, 0, 0)

# # Преобразование из кватерниона в углы Эйлера
# euler = euler_from_quaternion(quaternion)

# Простая функция "каллбек". Данная функция вызываеться
# в момент когда появились данные. В нашем примере
# выводи данные на экран
def callback(msg):
    # rostopic echo /odom
    print "X = ",  msg.pose.pose.position.x
    print "Y = ",  msg.pose.pose.position.y
    print "theta = ", quaternion_to_theta(msg.pose.pose.orientation)

# Инициализируем ноду ROS
rospy.init_node('temp_odom_subscr_1')
# Создаем подписчиака, в параметрах указываем
# Название топика, тип сообщения, имя функцим каллбека
sub = rospy.Subscriber('odom', Odometry, callback)
# Выводим информационное сообщение
# print sub.header

rospy.loginfo("I am a odom_subscriber_1")
# # Передаем у
rospy.spin()

# Then do
# rostopic pub /cpu_temp_1 std_msgs/Float32 55 -r10
# from another terminal