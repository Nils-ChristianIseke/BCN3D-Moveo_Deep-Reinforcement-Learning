#!/usr/bin/env python3

import numpy as np
import rospy
from gazebo_msgs.srv import GetWorldProperties, GetModelState, SetModelState
import sys
import random
from gazebo_msgs.msg import ModelState
import math


rospy.init_node('setPose')
_object_name = "goalPoint"
world_specs = rospy.ServiceProxy(
            '/gazebo/get_world_properties', GetWorldProperties)()
time = 0
model_names = world_specs.model_names
get_model_state = rospy.ServiceProxy(
             '/gazebo/get_model_state', GetModelState)
for model_name in model_names:
    if model_name == _object_name:
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
            resp = set_state(state_msg )
            rospy.logwarn("setting new goalpoint")
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
