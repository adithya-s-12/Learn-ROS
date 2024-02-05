#!/usr/bin/env python3

from math import pi
import rospy
from geometry_msgs.msg import Twist
from robot_pkg.srv import draw_polygon, draw_polygonResponse

class drawServer():
    
    def __init__(self):
        rospy.init_node('draw_server')
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(1)  
        self.velocity = Twist()
        self.polygon_service = rospy.Service('draw_polygon', draw_polygon, self.draw) 

    def draw(self, req):
        angle = 2*pi/req.n
        duration = 1
        for _ in range(req.n):
            tO = rospy.Time.now().to_sec()
            while rospy.Time.now().to_sec()-tO<=duration:
                self.velocity.angular.z = angle
                self.pub.publish(self.velocity)
            self.velocity.angular.z = 0
            self.pub.publish(self.velocity)
            tO = rospy.Time.now().to_sec()
            while rospy.Time.now().to_sec()-tO<=duration:
                self.velocity.linear.x = 2
                self.pub.publish(self.velocity)
            self.velocity.linear.x = 0
            self.pub.publish(self.velocity)
        return draw_polygonResponse() 

if __name__ == '__main__':
    try:
        controller = drawServer()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass