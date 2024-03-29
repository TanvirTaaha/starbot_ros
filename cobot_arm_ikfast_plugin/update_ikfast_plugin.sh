search_mode=OPTIMIZE_MAX_JOINT
srdf_filename=cobot.srdf
robot_name_in_srdf=cobot
moveit_config_pkg=cobot_moveit_config
robot_name=cobot
planning_group_name=arm
ikfast_plugin_pkg=cobot_arm_ikfast_plugin
base_link_name=base_link
eef_link_name=end_effector
ikfast_output_path=/home/taaha/catkin_ws/src/cobot_arm_ikfast_plugin/src/cobot_arm_ikfast_solver.cpp

rosrun moveit_kinematics create_ikfast_moveit_plugin.py\
  --search_mode=$search_mode\
  --srdf_filename=$srdf_filename\
  --robot_name_in_srdf=$robot_name_in_srdf\
  --moveit_config_pkg=$moveit_config_pkg\
  $robot_name\
  $planning_group_name\
  $ikfast_plugin_pkg\
  $base_link_name\
  $eef_link_name\
  $ikfast_output_path
