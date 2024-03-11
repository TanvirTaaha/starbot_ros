# starbot_ros
### Academic project of BUET
- comfirm installation of `moveit`, `ros-controllers`, `gazebo-ros-pkgs` etc
- `filename` tag in gazebo plugins tags(major flaw of setup assistant because it is not filled in the auto generated file)
- `velocity` and `effort` limit must not be zero
- still I don't know what happened with effort controller(maybe effort limit was not enough to overcome friction limit). robot was slowly dropping down from it's position.
- `dynamic` tag with friction and damping is required.