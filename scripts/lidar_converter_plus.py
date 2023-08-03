#!/usr/bin/env python3

import rospy
from livox_ros_driver2.msg import CustomMsg
from livox_ros_driver2.msg import CustomPoint
from sensor_msgs.msg import Imu

new_cloud = CustomMsg()
cloud_converted = False
imu_converted = False

def convert_lidar(msg):
    global new_cloud
    global cloud_converted
    new_cloud = CustomMsg()
    new_cloud.header = msg.header
    new_cloud.timebase = msg.timebase
    new_cloud.point_num = 0
    new_cloud.lidar_id = msg.lidar_id
    new_cloud.rsvd = msg.rsvd
    for point in msg.points:
        # if point.x > -0.5 and point.x < 0 and point.y > -0.275 and point.y < 0.275 and point.z < 0.6:
            # continue
        new_point = CustomPoint()

        new_point.offset_time = point.offset_time
        new_point.reflectivity = point.reflectivity
        new_point.tag = point.tag
        new_point.line = point.line

        new_point.x = point.y
        new_point.y = -point.x
        new_point.z = point.z

        new_cloud.points.append(new_point)
        new_cloud.point_num += 1
    cloud_converted = True

def convert_Imu(msg):
    global new_imu
    global imu_converted

    new_imu = Imu()
    new_imu.header = msg.header
    new_imu.orientation = msg.orientation
    new_imu.orientation_covariance = msg.orientation_covariance

    new_imu.angular_velocity.x = msg.angular_velocity.y
    new_imu.angular_velocity.y = -msg.angular_velocity.x
    new_imu.angular_velocity.z = msg.angular_velocity.z
    new_imu.angular_velocity_covariance = msg.angular_velocity_covariance

    new_imu.linear_acceleration.x = msg.linear_acceleration.y
    new_imu.linear_acceleration.y = -msg.linear_acceleration.x
    new_imu.linear_acceleration.z = msg.linear_acceleration.z
    new_imu.linear_acceleration_covariance = msg.linear_acceleration_covariance
    imu_converted = True
    

if __name__ == "__main__":
    rospy.init_node("lidar_converter")
    sub = rospy.Subscriber("/livox/lidar", CustomMsg, convert_lidar, queue_size=100)
    sub = rospy.Subscriber("/livox/imu", Imu, convert_Imu, queue_size=100)
    DeltaTime = 0.01
    rate = rospy.Rate(1/DeltaTime)
    pub_cloud = rospy.Publisher("/new_lidar", CustomMsg, queue_size=100)
    pub_imu = rospy.Publisher("/new_imu", Imu, queue_size=100)
    while not rospy.is_shutdown():
        if cloud_converted is True:
            pub_cloud.publish(new_cloud)
            cloud_converted = False
        if imu_converted is True:
            pub_imu.publish(new_imu)
            imu_converted = False
            
        rate.sleep()
