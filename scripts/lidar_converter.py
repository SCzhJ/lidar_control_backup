#!/usr/bin/env python3

import rospy
from livox_ros_driver2.msg import CustomMsg
from livox_ros_driver2.msg import CustomPoint

new_cloud = CustomMsg()
converted = False

def get_lidar(msg):
    global new_cloud
    global converted
    new_cloud = CustomMsg()
    new_cloud.header = msg.header
    new_cloud.timebase = msg.timebase
    new_cloud.point_num = 0
    new_cloud.lidar_id = msg.lidar_id
    new_cloud.rsvd = msg.rsvd
    for point in msg.points:
        if point.x > -0.5 and point.x < 0 and point.y > -0.275 and point.y < 0.275 and point.z < 0.6:
            continue
        new_cloud.points.append(point)
        new_cloud.point_num += 1
    converted = True


if __name__ == "__main__":
    rospy.init_node("lidar_converter")
    sub = rospy.Subscriber("/livox/lidar", CustomMsg, get_lidar, queue_size=100)
    DeltaTime = 0.01
    rate = rospy.Rate(1/DeltaTime)
    pub = rospy.Publisher("/new_lidar", CustomMsg, queue_size=100)
    while not rospy.is_shutdown():
        if converted is True:
            pub.publish(new_cloud)
            converted = False
        rate.sleep()
