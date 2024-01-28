#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16
from std_msgs.msg import Bool
from robot_pkg.msg import custom_message

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) 
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

def number_publisher():
    pub = rospy.Publisher('number_out', Int16, queue_size=1)
    rospy.init_node('int_publisher', anonymous=True)
    rate = rospy.Rate(10) 
    num_msg = 0
    while not rospy.is_shutdown():
        pub.publish(num_msg) #does not print msgs, only send to publisher to listen
        rate.sleep()
        num_msg += 1
        
def true_or_false():
    pub = rospy.Publisher('true_or_false', Bool, queue_size=10)
    rospy.init_node('boolean_publisher', anonymous=True)
    rate = rospy.Rate(10)
    decision = False
    while not rospy.is_shutdown():
        pub.publish(decision)
        rate.sleep()
        if not decision:
            decision = True
        else:
            decision = False       

def my_custom_msg():
    pub = rospy.Publisher("custom_msg",custom_message, queue_size=10)
    rospy.init_node("custom_msg_publisher")
    rate = rospy.Rate(10)
    
    msg = custom_message()
    msg.id.data = 1
    msg.name.data = "hello"
    msg.employed.data = False
    msg.location.x = 0
    msg.location.y = 0
    msg.location.theta = 0
    
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()
        if not msg.employed.data:
            msg.employed.data = True
        else:
            msg.employed.data = False
        msg.id.data += 1
        msg.location.x += 2
        msg.location.y += 3
        msg.location.theta += 1
        rospy.loginfo("in this loop")
    
    
if __name__ == '__main__':
    try:
        my_custom_msg()
    except rospy.ROSInterruptException:
        pass