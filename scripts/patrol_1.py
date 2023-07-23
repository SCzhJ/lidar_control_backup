#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PointStamped


if __name__ == "__main__":
    rospy.init_node("patrol_1")
    pub = rospy.Publisher("/way_point", PointStamped, queue_size=100)
    msg = PointStamped()
    msg.header.frame_id = "map"
    msg.point.z = 0
    DeltaTime = 0.01
    rate = rospy.Rate(1/DeltaTime)

    PatrolIntervalTime = 10
    state = False
    CurrentTime = PatrolIntervalTime

    while not rospy.is_shutdown():
        if CurrentTime <= 0:
            CurrentTime = PatrolIntervalTime
            if state:
                msg.point.x = 2
                msg.point.y = 0
            else:
                msg.point.x = -2
                msg.point.y = 0
            state = not state
            pub.publish(msg)
        CurrentTime -= DeltaTime
        rate.sleep()


