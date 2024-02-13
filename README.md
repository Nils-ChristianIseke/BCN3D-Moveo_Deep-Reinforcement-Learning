## BCN3D-Moveo, Deep Learning
This repos aimed to enable deep learning for the open source-robotic arm BCN3D-Moveo.


### Prerequisites
1. Installation of ROS Noetic
```
http://wiki.ros.org/noetic/Installation
```
2. Installation of Gazebo

```
http://gazebosim.org/tutorials?cat=install
```

### Setup
1. Create a catkin workspace
```
http://wiki.ros.org/catkin/Tutorials/create_a_workspace
```
2. Clone this repository into the created workspace
``` 
git clone https://github.com/SLINIS/Moveo_RL.git
```
3. Build the project
```
catkin_make
```  
4. Source workspace
```
cd catkin_ws
source devel/setup.bash
```

### Start the Simulation
All launch files are placed in the moveo_moveit_config package. At the moment 3 different simulations for three different tasks exist, which can be launched by executing the commands provided below:
1. Inverse Kinematic 
```
roslaunch moveo_moveit_config ik_training.launch
```
2. Push Task
```
roslaunch moveo_moveit_config push_training.launch
```
3. Pick Task
```
roslaunch moveo_moveit_config pick_training.launch
```

To start the training the following command needs to be executed:

```
python src/moveo_training/scripts/train_eval.py   --root_dir=~/sac/gym/MovoePush-v0/   --alsologtostderr
```

The flag --root_dir specifies the placement of the directory, where all data of the training and evaluation is placed.
By using tensorboard the training and evaluation metrics can be plotted.

```
tensorboard --logdir ~/sac/gym/MovoePush-v0/ --port 2223 &
```
