#! /usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg

class MoveoCommander(object):

    def __init__(self):

        moveit_commander.roscpp_initialize(sys.argv)

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        print("###### Setting Group Moveit with 30 seconds wait...")
        self.group = moveit_commander.MoveGroupCommander("arm", wait_for_servers=30.0)

        self.pose_target = geometry_msgs.msg.Pose()

    def move_ee_to_pose(self, ee_pose):

        self.pose_target.orientation.w = ee_pose.orientation.w
        self.pose_target.position.x = ee_pose.position.x
        self.pose_target.position.y = ee_pose.position.y
        self.pose_target.position.z = ee_pose.position.z
        self.group.set_pose_target(self.pose_target)
        self.execute_trajectory()

        return True, "Everything went OK"

    def move_joints_traj(self, joint_positions):

        self.group_variable_values = self.group.get_current_joint_values()
        self.group_variable_values[0] = joint_positions[0]
        self.group_variable_values[1] = joint_positions[1]
        self.group_variable_values[2] = joint_positions[2]
        self.group_variable_values[3] = joint_positions[3]
        self.group_variable_values[4] = joint_positions[4]
        self.group.set_joint_value_target(self.group_variable_values)
        self.execute_trajectory()

        return True, "Trajectory executed OK"

    def execute_trajectory(self):

        self.plan = self.group.plan()
        self.group.go(wait=True)

    def get_ee_pose(self):

        gripper_pose = self.group.get_current_pose()

        return gripper_pose.pose

    def get_ee_rpy(self):

        gripper_rpy = self.group.get_current_rpy()
        roll = gripper_rpy[0]
        pitch = gripper_rpy[1]
        yaw = gripper_rpy[2]

        return [roll,pitch,yaw]


def test_movements():

    print("All Zeros joints Pose")
    position=[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    #position=[ 1.3200097856338848, 1.399990714155538, -0.19990423826440207, 1.7199628687377988, 5.368386582382811e-06, 1.66000908212966, -6.523043055040034e-06]
    traj_serv_object.move_joints_traj(position)

    print("Tuck ee Pose")
    ee_pose = geometry_msgs.msg.Pose()

    ee_pose.position.x = 0.0533894092376196
    ee_pose.position.y = -0.139545762668953
    ee_pose.position.z = 0.5712545395231896
    ee_pose.orientation.x = 0.45831588421891434
    ee_pose.orientation.y = -0.5045935352890618
    ee_pose.orientation.z = 0.5093392311611178
    ee_pose.orientation.w = 0.5252670387691603


    traj_serv_object.move_ee_to_pose(ee_pose)

if __name__ == "__main__":

    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    traj_serv_object = MoveoCommander()

    print("All Zeros ee Pose")
    ee_pose = geometry_msgs.msg.Pose()

    ee_pose.position.x = 0.9616499977481227
    ee_pose.position.y = 1.7153330350514874e-05
    ee_pose.position.z = 0.7860662143235629
    ee_pose.orientation.x = 0.005094929484692078
    ee_pose.orientation.y = -5.475560224745837e-05
    ee_pose.orientation.z = 9.29634914807148e-06
    ee_pose.orientation.w = 0.9999870192202236

    traj_serv_object.move_ee_to_pose(ee_pose)

    print(str(traj_serv_object.get_ee_pose()))
    print(str(traj_serv_object.get_ee_rpy()))

    print("All Zeros ee Pose - delta")
    ee_pose.position.x -= 0.1
    traj_serv_object.move_ee_to_pose(ee_pose)

    print(str(traj_serv_object.get_ee_pose()))
    print(str(traj_serv_object.get_ee_rpy()))