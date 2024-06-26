# starbot_ros

 Academic project of BUET

## Things that are must after `moveit_setup_assistant`

- install dependencies(in your ws directory): `rosdep install --from-paths src --ignore-src -r -y`
- comfirm installation of `moveit`, `ros-controllers`, `gazebo-ros-pkgs` etc
- `filename` tag in gazebo plugins tags(major flaw of setup assistant because it is not filled in the auto generated file)
- `velocity` and `effort` limit must not be zero
- still I don't know what happened with effort controller(maybe effort limit was not enough to overcome friction limit). robot was slowly dropping down from it's position.
- `dynamic` tag with friction and damping is required.

## Necessary(safe to) installs

- `ros-$ROS_DISTRO-ros-control`
- `ros-$ROS_DISTRO-ros-controllers`
- `ros-$ROS_DISTRO-gazebo-*`
- `ros-$ROS_DISTRO-moveit`
- `ros-$ROS_DISTRO-moveit-*`
- `ros-$ROS_DISTRO-rqt-*`
  
> joint_state_controller is a common controller needed to publish joint state(need for gazebo or real not sure, maybe both)
> but controllers for individual joints can be configured one by one or all at ones(I guess)

 This error may be ignored:

> No p gain specified for pid.  Namespace: /gazebo_ros_control/pid_gains/base_stand__base

For over all walkthorugh:

- For first time learners: Simulate a single joint(dc motor with encoder) with simple demo urdf:[Youtube](https://youtu.be/88VbbSiAZCk?si=IvtenBTyQzSg1JL4) [Github](https://github.com/bandasaikrishna/ros_control_example.git) [Article(Recommended)](https://www.rosroboticslearning.com/ros-control)
- For 6dof robot and **hardware interface** [Youtube](https://youtu.be/G_EvFqO7VHM?si=I-jOijv5H4FKw3em) [Github](https://github.com/bandasaikrishna/6-DOF_Manipulator.git) [Article](https://www.rosroboticslearning.com/)
- Follow this repo [import_your_custom_urdf_package_to_ROS](https://github.com/ageofrobotics/import_your_custom_urdf_package_to_ROS-main.git) with this [youtube playlist](https://youtube.com/playlist?list=PLeEzO_sX5H6TBD6EMGgV-qdhzxPY19m12&si=NdK21Pe5GSLZaA60)

A good playlist for ros control: [ROS Control](https://youtube.com/playlist?list=PL0LxxVxIWiJJOgmy3xeIUUMxGZBvcpmaT&si=EyB8C3QI9dOkcytn)

## IKFast Plugin for Moveit

As this arm is only 4DOF moveit's kdl kinematic solver won't work.
[Official tutorial for creating ikfast plugin](https://ros-planning.github.io/moveit_tutorials/doc/ikfast/ikfast_tutorial.html)
The docker way is recommended:

- You need to provide the urdf file(xacro won't work)

    ```bash
  rosrun xacro xacro -o /tmp/$MYROBOT_NAME.urdf $MYROBOT_NAME.urdf.xacro
    ```

- You have to select IK Type from [this page](http://openrave.org/docs/latest_stable/openravepy/ikfast/#ik-types) for this project
-
