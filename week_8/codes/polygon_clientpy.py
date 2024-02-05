#!/usr/bin/env python3
import sys
import rospy
from robot_pkg.srv import draw_polygon, draw_polygonResponse

def draw_polygon_client(n):
    rospy.wait_for_service('draw_polygon')
    try:
        polygon = rospy.ServiceProxy('draw_polygon', draw_polygon)
        resp = polygon(n)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":
    n = int(sys.argv[1])
    draw_polygon_client(n)
    print("Requesting n:%f"%(n))