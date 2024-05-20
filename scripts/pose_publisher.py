#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose
from dynamic_reconfigure.server import Server
from robot_pose_pub.cfg import TestConfig

class PosePublisher:
    def __init__(self):
        self.publisher = rospy.Publisher('/robot_pose', Pose, queue_size=10)
        self.rate = rospy.Rate(10)  # 10Hz
        self.pose = Pose()
        self.server = Server(TestConfig, self.dynamic_reconfigure_callback)
        

    def dynamic_reconfigure_callback(self, config, level):
        rospy.loginfo("Reconfigure Request: x={x}, y={y}, z={z}, qx={qx}, qy={qy}, qz={qz}, qw={qw}".format(**config))
        self.pose.position.x = config['x']
        self.pose.position.y = config['y']
        self.pose.position.z = config['z']
        self.pose.orientation.x = config['qx']
        self.pose.orientation.y = config['qy']
        self.pose.orientation.z = config['qz']
        self.pose.orientation.w = config['qw']
        return config

    def run(self):
        while not rospy.is_shutdown():
            self.publisher.publish(self.pose)
            self.rate.sleep()

if __name__ == '__main__':
    rospy.init_node('pose_publisher')
    pp = PosePublisher()
    pp.run()