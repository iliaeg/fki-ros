#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy

from std_msgs.msg import String

class GreetingWorker(object):

    def __init__(self):
        self.pub = rospy.Publisher('/greeting', String, queue_size=10)

    def sayHello(self, income_msg):
        self.pub.publish('Hello, {}'.format(income_msg.data))

if __name__ == '__main__':

    gretter = GreetingWorker()

    rospy.init_node('creeting_node')
    rospy.loginfo("Start Greeting Node")
    rospy.Subscriber("/ilia_name", String, gretter.sayHello)
    rospy.spin()