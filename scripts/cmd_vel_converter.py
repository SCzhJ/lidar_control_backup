#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped

lin_x = 0
lin_y = 0
lin_z = 0
ang_x = 0
ang_y = 0
ang_z = 0
history = [0]*6 # 10; 

def GetVel(msg):
    global history
    global lin_x
    global lin_y
    global lin_z
    global ang_x
    global ang_y
    global ang_z
    
    lin_x = msg.twist.linear.x
    lin_y = msg.twist.linear.y
    # lin_z = msg.twist.linear.z
    # ang_x = msg.twist.angular.x
    # ang_y = msg.twist.angular.y
    ang_z = msg.twist.angular.z
    history = history[1:]+[round(ang_z,2)]

if __name__=="__main__":
    rospy.init_node("cmd_vel_converter")
    sub = rospy.Subscriber("new_vel", TwistStamped, GetVel, queue_size=100)
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=100)
    deltaTime = 0.05
    rate = rospy.Rate(1/deltaTime)

    msg = Twist()

    while not rospy.is_shutdown():
        # history = history[1:]+[round(ang_z,2)]
        #history = history[1:]+[round(ang_z/2,2)]
        # msg.angular.z = round(sum(history)/3,2)
        # msg.angular.z = round(ang_z,2)
        msg.linear.x = round(lin_x, 2)
        msg.linear.y = round(lin_y, 2)
        msg.angular.z = round(sum(history)/6,2)
        pub.publish(msg)
        rate.sleep()
