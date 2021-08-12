cmake_minimum_required(VERSION 3.0.2)
project(moveo_moveit)


# find_package(Eigen3 REQUIRED)

# Eigen 3.2 (Wily) only provides EIGEN3_INCLUDE_DIR, not EIGEN3_INCLUDE_DIRS
# if(NOT EIGEN3_INCLUDE_DIRS)
#   set(EIGEN3_INCLUDE_DIRS ${EIGEN3_INCLUDE_DIR})
# endif()
# adde rosserial_arduino and rosserial_client
find_package(
    catkin REQUIRED COMPONENTS
    # rosserial_arduino
    # rosserial_client
    roscpp
    rospy
    sensor_msgs
    moveit_core
    moveit_ros_planning
    moveit_ros_planning_interface
    pluginlib
    geometric_shapes
    moveit_visual_tools
    message_generation
    std_msgs
)


# find_package(Boost REQUIRED system filesystem date_time thread)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  ArmJointState.msg
)


# adde rosserial_generate and comfigure
# rosserial_generate_ros_lib(
#   PACKAGE rosserial_arduino
#   SCRIPT make_libraries.py
# )

# rosserial_configure_client(
#   DIRECTORY firmware
#   TOOLCHAIN_FILE ${ROSSERIAL_ARDUINO_TOOLCHAIN}
# )
################################################
## Declare ROS messages, services and actions ##
################################################




## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  # sensor_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS
    moveit_core
    moveit_ros_planning_interface
    interactive_markers
    message_runtime
    std_msgs
  DEPENDS
    EIGEN3
)

###########
## Build ##
###########

include_directories(SYSTEM ${Boost_INCLUDE_DIR} ${EIGEN3_INCLUDE_DIRS})
include_directories(${catkin_INCLUDE_DIRS})
link_directories(${catkin_LIBRARY_DIRS})

## Declare a C++ executable
add_executable(moveit_convert src/moveit_convert.cpp)
add_executable(move_group_1 src/move_group_interface_coor_1.cpp)

add_dependencies(moveit_convert moveo_moveit_generate_messages_cpp)
## Specify libraries to link a library or executable target against
catkin_install_python(PROGRAMS scripts/moveo_objrec_publisher.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

target_link_libraries(moveit_convert
  ${catkin_LIBRARIES}
)
target_link_libraries(move_group_1
  ${catkin_LIBRARIES}
)


