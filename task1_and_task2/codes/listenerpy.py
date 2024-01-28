#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16
from std_msgs.msg import Bool
from robot_pkg.msg import custom_message

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def num_callback(data):
    rospy.loginfo("the num is %d", data.data)
    
def true_or_false_callback(data):
    rospy.loginfo("the decision is %s", data.data)
    
def custom_callback(data):
    rospy.loginfo("ID-number: %d, Name: %s, Employment status: %s, location(x,y,theta): %d,%d,%d", data.id.data, data.name.data, data.employed.data, data.location.x, data.location.y, data.location.theta)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", String, callback)
    rospy.spin()

def number_listener():
    rospy.init_node('int_subscriber', anonymous=True) #node name(will be displayed in node info as sub)
    rospy.Subscriber("number_out", Int16, num_callback) # topic of the conversation
    rospy.spin()
    
def bool_listener():
    rospy.init_node("boolean_subscriber", anonymous=True)
    rospy.Subscriber("true_or_false", Bool, true_or_false_callback)
    rospy.spin()
    
def custom_listener():
    rospy.init_node("custom_msg_subscriber")
    rospy.Subscriber("custom_msg",custom_message,custom_callback)
    rospy.spin()
    
if __name__ == '__main__':
    custom_listener()
    