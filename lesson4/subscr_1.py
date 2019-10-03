#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Подключаем библиотеку для работы с ROS
import rospy
# Импортируем обьект для работы с нужными нам сообщениями
from std_msgs.msg import Float32

# Простая функция "каллбек". Данная функция вызываеться
# в момент когда появились данные. В нашем примере
# выводи данные на экран
def callback(msg):
  print msg.data

# Инициализируем ноду ROS
rospy.init_node('temp_subscriber')
# Создаем подписчиака, в параметрах указываем
# Название топика, тип сообщения, имя функцим каллбека
sub = rospy.Subscriber('cpu_temp', Float32, callback)
# Выводим информационное сообщение
rospy.loginfo("I am a subscriber")
# Передаем у
rospy.spin()

# Then do
# rostopic pub /cpu_temp std_msgs/Float32 55 -r10
# from another terminal