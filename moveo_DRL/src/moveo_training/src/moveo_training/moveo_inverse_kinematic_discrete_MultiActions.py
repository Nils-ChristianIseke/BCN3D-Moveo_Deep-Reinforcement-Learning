#! /usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

tf.compat.v1.enable_v2_behavior()



from gym import utils
import math
import rospy
from src.moveo_training.src.moveo_training.cube_positions import Obj_Pos
from gym import spaces
from src.moveo_training.src.moveo_training import moveo_env
from gym.envs.registration import register
import numpy as np

max_episode_steps = 1 # Can be any Value

register(
        id='MoveoIK_discrete_MultiActions-v0',
        entry_point='src.moveo_training.src.moveo_training.moveo_inverse_kinematic_discrete_MultiActions:MoveoIKEnv',
        max_episode_steps=max_episode_steps,
    )


class MoveoIKEnv(moveo_env.MoveoEnv, utils.EzPickle):
    def __init__(self):
        
        # print ("Entered InverseKinematics Env")
        self.obj_positions = Obj_Pos(object_name="goalPoint")

        self.get_params()

        moveo_env.MoveoEnv.__init__(self)
        utils.EzPickle.__init__(self)

        self.gazebo.unpauseSim()

       
        self.action_space = spaces.MultiDiscrete((270,270,270,270,270))
        # self.action_space = spaces.Box(
        #     low=self.position_joints_min,
        #     high=self.position_joints_max, shape=(self.n_actions,),
        #     dtype=np.float32
        # )
        
        # observations_high_dist_x = np.array([self.max_distance])
        # observations_low_dist_x = np.array([0.0])
        # observations_high_dist_y = np.array([self.max_distance])
        # observations_low_dist_y = np.array([0.0])
        # observations_high_dist_z = np.array([self.max_distance])
        # observations_low_dist_z = np.array([0.0])
        observation_max_dist = np.array([2])
        observation_min_dist = np.array([0])
        

        observations_max_cube_x =np.array([1.0])
        observations_max_cube_y =np.array([1.0])
        observations_max_cube_z =np.array([1.0])
        observations_min_cube_x =np.array([-1.0])
        observations_min_cube_y =np.array([-1.0])
        observations_min_cube_z =np.array([-1.0])
        
        # observations_high_speed = np.array([self.max_speed])
        # observations_low_speed = np.array([0.0])

        # observations_ee_max = np.array([1])
        # observations_ee_min = np.array([-1])

        # high = np.concatenate([observations_max_cube_x,observations_max_cube_y,observations_max_cube_z,observation__max_dist,observations_ee_max,observations_ee_max,observations_ee_max])
        # low = np.concatenate([observations_min_cube_x,observations_min_cube_y,observations_min_cube_z,observation_min_dist,observations_ee_min,observations_ee_min,observations_ee_min])

        high = np.concatenate([ observation_max_dist,observations_max_cube_x,observations_max_cube_y,observations_max_cube_z])
        low = np.concatenate([observation_min_dist, observations_min_cube_x,observations_min_cube_y,observations_min_cube_z])
        self.observation_space = spaces.Box(low, high)

    def get_params(self):
        """
        get configuration parameters

        """
        self.sim_time = rospy.get_time()
        self.n_actions = 1
        self.n_observations = 3
        self.position_joints_max = 2.356
        self.position_joints_min = -2.356

        self.init_pos = {
                "Joint_1": 0.0,
                "Joint_2": 0.0,
                "Joint_3": 0.0,
                "Joint_4": 0.0,
                "Joint_5": 0.0,
                }
        
        self.setup_ee_pos = {"x": 0,
                            "y": 0,
                            "z": 0}
        self.impossible_movement_punishement = -1000
        self.max_distance_to_Goal= 0.05
   

    def _set_init_pose(self):
        self.gazebo.unpauseSim()
        if not self.set_trajectory_joints(self.init_pos):
            assert False, "Initialisation is failed...."

    def _init_env_variables(self):
        """
        Inits variables needed to be initialised each time we reset at the start
        :return:
        """
        # rospy.logdebug("Init Env Variables...")
        # rospy.logdebug("Init Env Variables...END")

    def _set_action(self, action):
       
        self.new_pos = {
                "Joint_1": float((action[0]-135)/180*math.pi),
                "Joint_2": float((action[1]-135)/180*math.pi),
                "Joint_3": float((action[2]-135)/180*math.pi),
                "Joint_4": float((action[3]-135)/180*math.pi),
                "Joint_5": float((action[4]-135)/180*math.pi),
                }


        self.movement_result = self.set_trajectory_joints(self.new_pos)


    def _get_obs(self):
        """
        It returns the Position of the TCP/EndEffector as observation.
        And the speed of cube
        Orientation for the moment is not considered
        """
        self.gazebo.unpauseSim()
        grip_pose = self.get_ee_pose()
        ee_array_pose = [grip_pose.position.x, grip_pose.position.y, grip_pose.position.z]

      
        # the pose of the goalPoint 
        object_data = self.obj_positions.get_states()

        # position GoalPoint
        object_pos = object_data[:3]
        distance_from_goal = self.calc_dist(object_pos,ee_array_pose)

        # We state as observations the distance form goal, the speed of goal and the z postion of the end effectors
        # observations_obj = np.array([object_pos[0],object_pos[1],object_pos[2],distance_from_goal,ee_array_pose[0],ee_array_pose[1],ee_array_pose[2]])
        observations_obj = np.array([distance_from_goal,object_pos[0],object_pos[1],object_pos[2]])
        return  observations_obj
    
    def calc_dist(self,p1,p2):
        """
        d = ((2 - 1)2 + (1 - 1)2 + (2 - 0)2)1/2
        """
       
        x_d = math.pow(p1[0] - p2[0],2)
        y_d = math.pow(p1[1] - p2[1],2)
        z_d = math.pow(p1[2] - p2[2],2)
        d = math.sqrt(x_d + y_d + z_d)

        return d

    
    def get_elapsed_time(self):
        """
        Returns the elapsed time since the beginning of the simulation
        Then maintains the current time as "previous time" to calculate the elapsed time again
        """
        current_time = rospy.get_time()
        dt = self.sim_time - current_time
        self.sim_time = current_time
        return dt

    def _is_done(self, observations):
        """
        If the latest Action didnt succeed, it means that tha position asked was imposible therefore the episode must end.
        It will also end if it reaches its goal.
        """

       
        # distance = observations[0]
        distance = observations[0]
        # Did the movement fail in set action?
        done_fail = not(self.movement_result)

        done_sucess = distance <= self.max_distance_to_Goal

        # print(">>>>>>>>>>>>>>>>done_fail="+str(done_fail)+",done_sucess="+str(done_sucess))
        # If it moved or the arm couldnt reach a position asced for it stops
        done = done_fail or done_sucess

        return done

    def _compute_reward(self, observations, done):
        """
        Reward moving the cube
        Punish movint to unreachable positions
        Calculate the reward: binary => 1 for success, 0 for failure
        """
        distance =  observations[0]


        # Did the movement fail in set action?
        done_fail = not(self.movement_result)

        done_sucess = distance <= self.max_distance_to_Goal
        # print("Distanz zum Ziel= "+ str(distance))
        if done_fail:
            # We punish that it tries sto move where moveit cant reach
            reward = self.impossible_movement_punishement
            # print("Bestrafung für unmögliche Kombination an Gelenkwinkel! Reward= ", reward)
        else:
            if done_sucess:
                #It reached the goal
                reward = -1*self.impossible_movement_punishement
                print("Ziel wurde erreicht Reward= ", reward)
            else:
                reward = -distance*10
                # print("Ziel wurde nicht erreicht, Reward= ", reward)
        return reward