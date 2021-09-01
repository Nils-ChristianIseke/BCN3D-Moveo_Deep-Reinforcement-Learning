#!/usr/bin/env python

import numpy as np
import rospy
from gazebo_msgs.srv import GetWorldProperties, GetModelState, SetModelState
import sys
import random
from gazebo_msgs.msg import ModelState 
import math
class Obj_Pos(object):
    """
    This object maintains the pose and rotation of the cube in a simulation through Gazebo Service

    """

    def __init__(self, object_name):
        self._object_name = object_name
        world_specs = rospy.ServiceProxy(
            '/gazebo/get_world_properties', GetWorldProperties)()
        self.time = 0
        self.model_names = world_specs.model_names
        self.get_model_state = rospy.ServiceProxy(
            '/gazebo/get_model_state', GetModelState)
        self.set_model_state = rospy.ServiceProxy('/gazebo/set_model_state',SetModelState)
        # self.set_states()
    def get_states(self):
        """
        Returns the ndarray of pose&rotation of the cube
        """
        for model_name in self.model_names:
            if model_name == self._object_name:
                data = self.get_model_state(
                    model_name, "world")  # gazebo service client
                return np.array([
                    data.pose.position.x,
                    data.pose.position.y,
                    data.pose.position.z,
                    data.twist.linear.x,
                    data.twist.linear.y,
                    data.twist.linear.z
                ])
    def set_states(self):
        # rospy.init_node('set_pose')
        for model_name in self.model_names:
            if model_name == self._object_name:
                state_msg = ModelState()
                state_msg.model_name = 'goalPoint'
                # this could be optimized to not allow goalPoints that are unreachable
                radius = random.uniform(-0.465,0.465)+0.235
                theta = random.uniform(-3.14,3.14)
                phi = random.uniform(-3.14,3.14)
                state_msg.pose.position.x = radius*math.sin(theta)*math.cos(phi)
                state_msg.pose.position.y = radius*math.sin(theta)*math.sin(phi)
                state_msg.pose.position.z = radius*math.cos(theta)
                state_msg.pose.orientation.x = 0
                state_msg.pose.orientation.y = 0
                state_msg.pose.orientation.z = 0
                state_msg.pose.orientation.w = 0
                rospy.wait_for_service('/gazebo/set_model_state')
                try:
                    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
                    resp = set_state( state_msg )
                except rospy.ServiceException as e:
                    print("Service call failed: %s" % e)
if __name__ == "__main__":
    rospy.init_node("DemoCube test")
    obj_positions = Obj_Pos(object_name="demo_cube")
    st = obj_positions.get_states()
    r = rospy.Rate(5.0)
    while not rospy.is_shutdown():
        st = obj_positions.get_states()
        # print(st)
        r.sleep()
