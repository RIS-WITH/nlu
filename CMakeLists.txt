cmake_minimum_required(VERSION 3.0.2)
project(nlu)

# add_compile_options(-std=c++11)
find_package(catkin REQUIRED COMPONENTS
   roscpp
   rospy
   std_msgs
   message_generation
)

# ###############################################
# # Declare ROS messages, services and actions ##
# ###############################################
add_message_files(
   FILES
   Slot.msg
)

# # Generate services in the 'srv' folder
add_service_files(
   FILES
   NLUParsingService.srv
)

# # Generate added messages and services with any dependencies listed here
generate_messages(
   DEPENDENCIES
   std_msgs
)

# ##################################
# # catkin specific configuration ##
# ##################################
catkin_package(

   # INCLUDE_DIRS include
   # LIBRARIES nlu
   # CATKIN_DEPENDS roscpp rospy std_msgs
   # DEPENDS system_lib
)

# ############
# # Install ##
# ############
catkin_install_python(PROGRAMS
   scripts/node_nlu.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
