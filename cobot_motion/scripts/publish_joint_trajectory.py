import rospy
import numpy as np
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import String

angle_values = []
def create_values():
    global angle_values
    # Define parameters
    amplitude = np.pi / 2  # Amplitude (half pi)
    period = 10  # Period in seconds
    sampling_rate = 100  # Samples per second

    # Calculate time step between samples
    dt = 1.0 / sampling_rate

    # Create time vector
    time = np.arange(0, period, dt)

    # Generate sine wave values
    sine_values = amplitude * np.sin(2 * np.pi * time / period)

    # Print the sine wave values (optional)
    # print(sine_values)
    angle_values = sine_values


def publish_joint_command(pub, trajectory):
    global angle_values
    # Set the desired joint positions
    joint_names = [
        "base_stand__base",
        "base__shoulder",
        "shoulder__elbow",
        "elbow__end_effector",
    ]  # Replace with your actual joint names
    #   positions = [1.0, 0.5, -1.0, 2.0]

    # Create a JointTrajectoryPoint message
    trajectory.joint_names = joint_names

    for i, name in enumerate(trajectory.joint_names):
        pointi = JointTrajectoryPoint()
        pointi.time_from_start = rospy.Duration(0.1)
        pointi.positions = angle_values
        print("hi")
        trajectory.points.append(pointi)
    print(trajectory.points)

    # Set header information (optional)
    trajectory.header.stamp = rospy.Time.now()
    trajectory.header.frame_id = "base_link"  # Replace if needed
    print("hello")

    rate = rospy.Rate(1)
    # Publish the message
    while not rospy.is_shutdown():
        pub.publish(trajectory)
        # rospy.spin()
        rate.sleep()
    print("how are you")


if __name__ == "__main__":
    try:
        pub = rospy.Publisher("/arm_controller/command", JointTrajectory, queue_size=10)
        rospy.init_node("joint_trajectory_msg_publisher")
        create_values()

        trajectory = JointTrajectory()
        
        t = int(rospy.Time.now().secs)
        print(f"publishing1: {t}")
        publish_joint_command(pub, trajectory)
        
        print(f"publishing2: {t}")
    except rospy.ROSInterruptException:
        pass