#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import imageio
import IPython
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import pyvirtualdisplay

import tensorflow as tf

from tf_agents.agents.reinforce import reinforce_agent
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.networks import actor_distribution_network
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from tf_agents.policies import random_tf_policy
from tf_agents.metrics import tf_metrics
from tf_agents.drivers import dynamic_episode_driver

import rospy
import moveo_inverse_kinematic

tf.compat.v1.enable_v2_behavior()
 
env_name = "MoveoIK-v0" # @param {type:"string"}
num_iterations = 5 # @param {type:"integer"}
collect_episodes_per_iteration = 2 # @param {type:"integer"}
replay_buffer_capacity = 2000 # @param {type:"integer"}

fc_layer_params = (100,)

learning_rate = 1e-3# @param {type:"number"}
log_interval = 25 # @param {type:"integer"}
num_eval_episodes = 5 # @param {type:"integer"}
eval_interval = 50 # @param {type:"integer"}

def compute_avg_return(environment, policy, num_episodes=10):

    total_return = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return

    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]


# Please also see the metrics module for standard implementations of different
# metrics.

def collect_episode(environment, policy, num_episodes):

    episode_counter = 0
    environment.reset()

    while episode_counter < num_episodes:
        time_step = environment.current_time_step()
        action_step = policy.action(time_step)
        next_time_step = environment.step(action_step.action)
        traj = trajectory.from_transition(time_step, action_step, next_time_step)

        # Add trajectory to the replay buffer
        replay_buffer.add_batch(traj)

        if traj.is_boundary():
            episode_counter += 1


# This loop is so common in RL, that we provide standard implementations of
# these. For more details see the drivers module.



rospy.init_node("train_moveo_her")
train_py_env = suite_gym.load(env_name)
eval_py_env = suite_gym.load(env_name)

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)


actor_net = actor_distribution_network.ActorDistributionNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=fc_layer_params)









optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

train_step_counter = tf.compat.v2.Variable(0)

tf_agent = reinforce_agent.ReinforceAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    actor_network=actor_net,
    optimizer=optimizer,
    normalize_returns=True,
    train_step_counter=train_step_counter)

tf_agent.initialize()

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=tf_agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_capacity)


eval_policy = tf_agent.policy
collect_policy = tf_agent.collect_policy


    
# random_policy = random_tf_policy.RandomTFPolicy(action_spec=train_env.action_spec(),
#                                         time_step_spec=train_env.time_step_spec())

# num_episodes = tf_metrics.NumberOfEpisodes()
# env_steps = tf_metrics.EnvironmentSteps()
# observers = [num_episodes, env_steps]
# driver = dynamic_episode_driver.DynamicEpisodeDriver(
#     train_env, random_policy, observers, num_episodes=20)


# Initial driver.run will reset the environment and initialize the policy.
# final_time_step, policy_state = driver.run()

# print('final_time_step', final_time_step)
# print('Number of Steps: ', env_steps.result().numpy())
# print('Number of Episodes: ', num_episodes.result().numpy())

# try:
# %%time
# except:
# pass

# (Optional) Optimize by wrapping some of the code in a graph using TF function.
tf_agent.train = common.function(tf_agent.train)

# Reset the train step
tf_agent.train_step_counter.assign(0)

# Evaluate the agent's policy once before training.
avg_return = compute_avg_return(eval_env, tf_agent.policy, num_eval_episodes)
returns = [avg_return]

for _ in range(num_iterations):

# Collect a few episodes using collect_policy and save to the replay buffer.
    collect_episode(
        train_env, tf_agent.collect_policy, collect_episodes_per_iteration)

    # Use data from the buffer and update the agent's network.
    experience = replay_buffer.gather_all()
    print("Erfahrung", experience)
    train_loss = tf_agent.train(experience)
    replay_buffer.clear()

    step = tf_agent.train_step_counter.numpy()

    if step % log_interval == 0:
        print('step = {0}: loss = {1}'.format(step, train_loss.loss))

    if step % eval_interval == 0:
        avg_return = compute_avg_return(eval_env, tf_agent.policy, num_eval_episodes)
        print('step = {0}: Average Return = {1}'.format(step, avg_return))
        returns.append(avg_return)

       
