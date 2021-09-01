#include "ros/ros.h"
#include "sensor_msgs/JointState.h"
// #include "moveo_moveit/ArmJointState.h"
#include "math.h"

sensor_msgs::JointState arm_steps;
sensor_msgs::JointState total;

int stepsPerRevolution[5] = {2000,16000,132000,7000,30000};  // microsteps/revolution (using 16ths) from observation, for each motor
int joint_status = 0;
double cur_angle[5];
int joint_step[5];
double prev_angle[5] = {0,0,0,0,0}; 
double init_angle[5] = {0,0,0,0,0};
double total_steps[5] = {0,0,0,0,0};
int count = 0;

void cmd_cb(const sensor_msgs::JointState& cmd_arm)
{
  if (count==0){
    prev_angle[0] = cmd_arm.position[0];
    prev_angle[1] = cmd_arm.position[1];
    prev_angle[2] = cmd_arm.position[2];
    prev_angle[3] = cmd_arm.position[3];
    prev_angle[4] = cmd_arm.position[4];
    prev_angle[5] = cmd_arm.position[5];
  }

 
  arm_steps.position.resize(6);
  arm_steps.position[0] = (int)((cmd_arm.position[0]-prev_angle[0])*stepsPerRevolution[0]/(2*M_PI));
  arm_steps.position[1] = (int)((cmd_arm.position[1]-prev_angle[1])*stepsPerRevolution[1]/(2*M_PI));
  arm_steps.position[2] = (int)((cmd_arm.position[2]-prev_angle[2])*stepsPerRevolution[2]/(2*M_PI));
  arm_steps.position[3] = (int)((cmd_arm.position[3]-prev_angle[3])*stepsPerRevolution[3]/(2*M_PI));
  arm_steps.position[4] = (int)((cmd_arm.position[4]-prev_angle[4])*stepsPerRevolution[4]/(2*M_PI));
  arm_steps.position[5] = (int)((cmd_arm.position[5]-prev_angle[5])*stepsPerRevolution[5]/(2*M_PI));

  if (count!=0){
    prev_angle[0] = cmd_arm.position[0];
    prev_angle[1] = cmd_arm.position[1];
    prev_angle[2] = cmd_arm.position[2];
    prev_angle[3] = cmd_arm.position[3];
    prev_angle[4] = cmd_arm.position[4];
    prev_angle[5] = cmd_arm.position[5];
  }

  total.position.resize(6);
  total.position[0] += arm_steps.position[0];
  total.position[1] += arm_steps.position[1];
  total.position[2] += arm_steps.position[2];
  total.position[3] += arm_steps.position[3];
  total.position[4] += arm_steps.position[4];
  total.position[4] += arm_steps.position[5];
  count=1;
  joint_status=1;
}

int main(int argc, char **argv)
{
  
  ros::init(argc, argv, "moveo_moveit");
  ros::NodeHandle nh;
  ros::Subscriber sub = nh.subscribe("/joint_states",1000,cmd_cb);
  ros::Publisher pub = nh.advertise<sensor_msgs::JointState>("joint_steps",50);
  ros::Rate loop_rate(20);
  
  while (ros::ok())
  {
    if(joint_status==1)
      {
        joint_status = 0;
        pub.publish(total);
      }
    ros::spinOnce();
    loop_rate.sleep();  
  }
  return 0;
}
