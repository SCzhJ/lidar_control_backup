#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped


if __name__=="__main__":
    rospy.init_node("way_point_publisher")
    pub = rospy.Publisher("/way_point", PointStamped, queue_size=100)
    deltaTime = 3
    rate = rospy.Rate(1/deltaTime)
    x = 10
    y = 10
    z = 10

    msg = PointStamped()

    while not rospy.is_shutdown():
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/map"
        msg.point.x = x
        msg.point.y = y
        msg.point.z = z
        x+=1
        y+=1
        z+=1
        pub.publish(msg)
        rate.sleep()
