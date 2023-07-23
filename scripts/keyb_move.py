#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

x = 0.0
y = 0.0
z = 0.0
speed = 0.15
turn_speed = 1.0
angle = 0.0
patrol = False
current_time = 0
def changeVelocity(msg):
    global x
    global y
    global z
    global patrol
    global current_time
    inp = msg.data
    rospy.loginfo("%s",inp)
    if inp == 'p':
        patrol = True
    else:
        if inp == 'w':
            x += speed
            patrol = False
            current_time = 0
        elif inp == 's':
            x -= speed
            patrol = False
            current_time = 0
        elif inp == 'a':
            y += speed
            patrol = False
            current_time = 0
        elif inp == 'd':
            y -= speed
            patrol = False
            current_time = 0
        elif inp == 'l':
            z -= turn_speed
            patrol = False
            current_time = 0
        elif inp == 'j':
            z += turn_speed
            patrol = False
            current_time = 0
        elif inp == 'k':
            z = 0.0
            patrol = False
            current_time = 0
        elif inp == 'q':
            x = 0.0
            y = 0.0
            z = 0.0
            patrol = False
            current_time = 0

if __name__ == "__main__":
    rospy.init_node("keyb_move")
    sub = rospy.Subscriber("keyb_input", String, changeVelocity, queue_size=100)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=100)
    delta_time = 0.05
    rate = rospy.Rate(1/delta_time)
    patrol_time = 3
    direction = 1
    msg = Twist()
    msg.linear.x = 0.0
    msg.linear.y = 0.0
    msg.linear.z = 0.0
    msg.angular.x = 0.0
    msg.angular.y = 0.0
    msg.angular.z = 0.0

while not rospy.is_shutdown():
    if patrol == True:
        msg.linear.x = 0
        msg.linear.y = 4 * speed * direction
        msg.linear.z = 0
        if current_time > patrol_time:
            current_time = 0
            direction = -direction
        current_time += delta_time
        pub.publish(msg)
    else:
        msg.linear.x = x
        msg.linear.y = y
        msg.angular.z = z
        angle += z * 1/10
        rospy.loginfo("x: %.2f ,y: %.2f, z: %.2f, angle: %.2f ",x,y,z,angle)
        pub.publish(msg)
        rate.sleep()

