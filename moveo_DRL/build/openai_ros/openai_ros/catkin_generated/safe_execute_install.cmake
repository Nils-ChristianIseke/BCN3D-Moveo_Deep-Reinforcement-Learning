execute_process(COMMAND "/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/build/openai_ros/openai_ros/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/build/openai_ros/openai_ros/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
