import rospy
from geometry_msgs.msg import Twist

rospy.init_node('cmd_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(1)
cmdmove = Twist()
cmdmove.angular.z = 0.9

while not rospy.is_shutdown():
    pub.publish(cmdmove)
    print('moving')
    rate.sleep()