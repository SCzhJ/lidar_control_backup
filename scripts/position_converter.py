#! /usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry

pos_x = 0
pos_y = 0
pos_z = 0
ori_x = 0
ori_y = 0
ori_z = 0

def GetPos(msg):
    global pos_x
    global pos_y
    global pos_z
    global ori_x
    global ori_y
    global ori_z
    
    pos_x = msg.pose.pose.position.x
    pos_y = msg.pose.pose.position.y
    pos_z = msg.pose.pose.position.z
    ori_x = msg.pose.pose.orientation.x
    ori_y = msg.pose.pose.orientation.y
    ori_z = msg.pose.pose.orientation.z

if __name__ == "__main__":
    rospy.init_node("pos_converter")
    sub = rospy.Subscriber("aft_mapped_to_init", Odometry, GetPos, queue_size=100)
    pub = rospy.Publisher("position", Odometry, queue_size=100)
    rate = rospy.Rate(20)

    msg = Odometry()
    msg.pose.pose.position.x = pos_x
    msg.pose.pose.position.y = pos_y
    msg.pose.pose.position.z = pos_z
    msg.pose.pose.orientation.x = ori_x
    msg.pose.pose.orientation.y = ori_y
    msg.pose.pose.orientation.z = ori_z

    while not rospy.is_shutdown():
        msg.pose.pose.position.x = round(pos_x,2)
        msg.pose.pose.position.y = round(pos_y,2)
        msg.pose.pose.position.z = round(pos_z,2)
        msg.pose.pose.orientation.x = round(ori_x,2)
        msg.pose.pose.orientation.y = round(ori_y,2)
        msg.pose.pose.orientation.z = round(ori_z,2)
        pub.publish(msg)
        rate.sleep()
    
