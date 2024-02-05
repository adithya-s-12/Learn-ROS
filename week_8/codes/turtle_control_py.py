#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import curses
from math import atan2, sqrt

class controller:
    vel_x = 1.2
    z = 0.4
    pi = 3.14
    
    def __init__(self):
        pub_topic_name = '/turtle1/cmd_vel'
        sub_topic_name = '/turtle1/pose'

        self.pub = rospy.Publisher(pub_topic_name, Twist, queue_size=10)
        self.sub = rospy.Subscriber(sub_topic_name, Pose, self.pose_callback)
        self.velocity = Twist()
        self.location = Pose()
        self.velocity.linear.x = 0.0
        self.velocity.angular.z = 0.0
        self.rate = rospy.Rate(1)
        
    def key_pressed(self, stdscr):
        stdscr.clear()
        stdscr.refresh()
        return stdscr.getch()

    def key_pressed_wrapper(self, stdscr):
        while not rospy.is_shutdown():
            key = self.key_pressed(stdscr)
            self.move(key)

    def move(self, key):
        if key == curses.KEY_UP:
            self.velocity.linear.x = self.vel_x
            self.velocity.angular.z = 0
        elif key == curses.KEY_DOWN:
            self.velocity.linear.x = - self.vel_x
            self.velocity.angular.z = 0
        elif key == curses.KEY_LEFT:
            self.velocity.angular.z = self.z
            self.velocity.linear.x = 0
        elif key == curses.KEY_RIGHT:
            self.velocity.angular.z = -self.z
            self.velocity.linear.x = 0
        self.pub.publish(self.velocity)    
        if key == ord("c"):
            self.draw_circle()
        elif key == ord("d"):
            self.draw_D()
        elif key == ord("h"):
            self.draw_hexagon()

    def pose_callback(self, msg):
        self.location.x = msg.x
        self.location.y = msg.y
        self.location.theta = msg.theta

    def go_to_goal(self, x, y):
        while abs(x - self.location.x) > 0.05 or abs(y - self.location.y) > 0.05:
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

          
    def draw_circle(self):
        while not rospy.is_shutdown():
            self.velocity.angular.z = self.z
            self.velocity.linear.x = self.vel_x
            self.pub.publish(self.velocity)
            self.rate.sleep()
            
    def draw_D(self):
        self.go_to_goal(4, 2)
        self.rate.sleep()
        self.go_to_goal(4, 8)
        self.rate.sleep()
        duration = 1.5*(self.pi/self.z)
        tO = rospy.Time.now().to_sec()
        while abs(self.location.theta) > 0.1:
            self.velocity.angular.z = -self.z
            self.pub.publish(self.velocity)
        while rospy.Time.now().to_sec()-tO<=duration:
            self.velocity.angular.z = -self.z
            self.velocity.linear.x = self.vel_x
            self.pub.publish(self.velocity)    

    def draw_hexagon(self):
        self.go_to_goal(2.5, 5.5)
        self.go_to_goal(4, 8.1)
        self.go_to_goal(7, 8.1) 
        self.go_to_goal(8.5, 5.5)
        self.go_to_goal(7, 2.9)
        self.go_to_goal(4, 2.9) 
        self.go_to_goal(2.5, 5.5)
    
if __name__ == "__main__":
    try:
        rospy.init_node("controller")
        turtle_control = controller()
        curses.wrapper(turtle_control.key_pressed_wrapper)
    except rospy.ROSInterruptException:
        pass