#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import atan2, sqrt
from turtlesim.srv import Spawn,Kill
import random

class spawn_crash_kill:
    vel_x = 1.2
    z = 0.4
    pi = 3.14
    turtle_names = ['turtle1']
    
    def __init__(self):
        
        self.velocity = Twist()

        self.velocity.linear.x = 0.0
        self.velocity.angular.z = 0.0
        self.rate = rospy.Rate(1)
        
    def pose_callback(self, msg):
        self.location = msg
        
    def go_to_goal(self, x, y):
        sub_topic_name = f'/{self.turtle_names[0]}/pose'
        self.sub = rospy.Subscriber(sub_topic_name, Pose, self.pose_callback)
        self.location = Pose()
        while abs(x - self.location.x) > 0.05 or abs(y - self.location.y) > 0.05:
            print(self.location)
            angle = atan2(y - self.location.y, x - self.location.x)
            distance = sqrt((x - self.location.x)**2 + (y - self.location.y)**2)
            self.velocity.linear.x = 0
            self.velocity.angular.z = self.z * (angle - self.location.theta)

            if abs(angle - self.location.theta) <= 0.05:
                self.velocity.angular.z = 0

                if distance > 0.05:
                    self.velocity.linear.x = (self.vel_x / 2) * distance
                else:
                    self.velocity.linear.x = 0
                    break

            self.pub.publish(self.velocity)
            self.rate.sleep()
        self.pub.publish(self.velocity)
    
    def spawn_new(self,x,y,theta,name):
        try:
            spawn = rospy.ServiceProxy("/spawn",Spawn)
            self.turtle_names.append(name)
            spawn(x,y,theta,name)
            
        except rospy.ServiceException as e:
            rospy.logerr(e)        
    
    def kill_prev(self,x,y):
        pub_topic_name = f'/{self.turtle_names[0]}/cmd_vel'
        self.pub = rospy.Publisher(pub_topic_name, Twist, queue_size=10)
        self.go_to_goal(x,y)
        name = self.turtle_names.pop(0)
        try:
            kill = rospy.ServiceProxy("/kill",Kill)
            kill(name)            
        except rospy.ServiceException as e:
            rospy.logerr(e)
        
if __name__=="__main__":
    try:
        rospy.init_node("sck")
        smk = spawn_crash_kill()
        count = 1
        while not rospy.is_shutdown():
            x = random.randint(1,10)
            y = random.randint(1,10)
            theta = random.randint(1,2)
            count = count+1
            name = f'turtle{count}'
            smk.spawn_new(x,y,theta,name)
            print(smk.turtle_names)
            smk.kill_prev(x,y)
    except rospy.ROSInterruptException:
        pass