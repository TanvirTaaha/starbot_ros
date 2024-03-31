#include <cobot_motion/cobot_hw_interface.h>

CobotHWInterface::CobotHWInterface(ros::NodeHandle &nh) : _nh(nh)
{
    init();
    _controller_manager.reset(new controller_manager::ControllerManager(this, _nh));
    _loop_hz = 20;                                               // Hz
    ros::Duration update_period = ros::Duration(1.0 / _loop_hz); // seconds

    pub = _nh.advertise<cobot_motion::FourJoints>("/controller_to_hw", 10);
    client = _nh.serviceClient<cobot_motion::JointSrv>("hw_to_controller");

    _non_realtime_loop = _nh.createTimer(update_period, &CobotHWInterface::update, this);
}

CobotHWInterface::~CobotHWInterface()
{
}

void CobotHWInterface::init()
{
    _num_joints = 4;
    _joint_names[0] = "base__shoulder";
    _joint_names[1] = "base_stand__base";
    _joint_names[2] = "elbow__end_effector";
    _joint_names[3] = "shoulder__elbow";

    for (int i = 0; i < _num_joints; i++)
    {
        // Create and register joint state handles
        hardware_interface::JointStateHandle jointStateHandle(_joint_names[i], &_joint_positions[i], &_joint_velocities[i], &_joint_efforts[i]);
        _joint_state_interface.registerHandle(jointStateHandle);

        // Create a JointHandle (read and write) for each controllable joint
        // using the read-only joint handles within the JointStateInterface and
        // register them with the JointPositionInterface.
        hardware_interface::JointHandle jointPositionHandle(jointStateHandle, &_joint_position_commands[i]);
        _position_joint_interface.registerHandle(jointPositionHandle);
    }
    // Register the JointStateInterface containing the read only joints
    // with this robot's hardware_interface::RobotHW.
    registerInterface(&_joint_state_interface);
    // Register the JointPositionInterface containing the read/write joints
    // with this robot's hardware_interface::RobotHW.
    registerInterface(&_position_joint_interface);
    _joint_position_commands[0] = 0;
    _joint_position_commands[1] = 0;
    _joint_position_commands[2] = 0;
    _joint_position_commands[3] = 0;
}

void CobotHWInterface::update(const ros::TimerEvent &e)
{
    _elapsed_time = ros::Duration(e.current_real - e.last_real);
    read();
    _controller_manager->update(ros::Time::now(), _elapsed_time);
    write(_elapsed_time);
}

void CobotHWInterface::read()
{
    joints_read.request.req = 1.0;
    if (client.call(joints_read))
    {
        _joint_positions[0] = joints_read.response.joint1;
        _joint_positions[1] = joints_read.response.joint2;
        _joint_positions[2] = joints_read.response.joint3;
        _joint_positions[3] = joints_read.response.joint4;

        std::string log = "Joint positions: ";
        for (auto i : _joint_positions)
        {
            char s[10]; // not needed 10, just to make sure no error occurs(got core dumped before)
            sprintf(s, " %.2f", i);
            log += s;
        }
        // ROS_INFO("%s", log.c_str());
    }
    else
    {
        _joint_positions[0] = 0;
        _joint_positions[1] = 0;
        _joint_positions[2] = 0;
        _joint_positions[3] = 0;
        // ROS_ERROR("No response for joint position request.");
    }
}

void CobotHWInterface::write(ros::Duration elapsed_time)
{
    joints_pub.joint1 = angles::to_degrees(_joint_position_commands[0]);
    joints_pub.joint2 = angles::to_degrees(_joint_position_commands[1]);
    joints_pub.joint3 = angles::to_degrees(_joint_position_commands[2]);
    joints_pub.joint4 = angles::to_degrees(_joint_position_commands[3]);

    pub.publish(joints_pub);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "cobot_hw_interface");
    ros::NodeHandle nh;

    ros::MultiThreadedSpinner spinner(4);
    CobotHWInterface robot(nh);
    spinner.spin();
    return 0;
}