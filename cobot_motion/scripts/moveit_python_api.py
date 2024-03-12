import sys
import copy
import rospy
import moveit_msgs.msg
import geometry_msgs.msg
import moveit_commander
from colorama import Fore, Style
from math import pi, tau, dist, fabs, cos

from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list


class Robot(object):
    def __init__(self) -> None:
        super(Robot, self).__init__()
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python_interface_tutorial", anonymous=True)

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.move_group = moveit_commander.MoveGroupCommander("arm")

        self.display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )
        # We can get the name of the reference frame for this robot:
        self.planning_frame = self.move_group.get_planning_frame()
        # print("============ Planning frame: %s" % planning_frame)

        # We can also print the name of the end-effector link for this group:
        self.eef_link = self.move_group.get_end_effector_link()
        # print("============ End effector link: %s" % eef_link)

        # We can get a list of all the groups in the robot:
        self.group_names = self.robot.get_group_names()
        # print("============ Available Planning Groups:", robot.get_group_names())

        # Sometimes for debugging it is useful to print the entire state of the robot:
        # print(f"============ Printing robot state\n{self.robot.get_current_state()}")
        pass

    def oscillate(self):
        time_period = 20
        i = 0
        rate = rospy.Rate(1)
        for i in range(20):
            # We get the joint values from the group and change some of the values:
            joint_goal = self.move_group.get_current_joint_values()
            joint_goal[0] = 0
            joint_goal[1] = 0
            joint_goal[2] = 0
            # joint_goal[3] = pi/2 * cos(tau * i / time_period)
            joint_goal[3] = ((-1) ** i) * pi / 2
            print(f"{Fore.GREEN}{i}{Style.RESET_ALL}")
            i += 1

            # The go command can be called with joint values, poses, or without any
            # parameters if you have already set the pose or joint target for the group
            self.move_group.go(joint_goal, wait=True)
            # rate.sleep()

        # Calling ``stop()`` ensures that there is no residual movement
        self.move_group.stop()
        print(f"{Fore.CYAN}Done{Style.RESET_ALL}")

    def go_to_pose_goal(self):
        ## BEGIN_SUB_TUTORIAL plan_to_pose
        ##
        ## Planning to a Pose Goal
        ## ^^^^^^^^^^^^^^^^^^^^^^^
        ## We can plan a motion for this group to a desired pose for the
        ## end-effector:
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        pose_goal.position.x = 0.4
        pose_goal.position.y = 0.1
        pose_goal.position.z = 0.4

        self.move_group.set_pose_target(pose_goal)

        ## Now, we call the planner to compute the plan and execute it.
        # `go()` returns a boolean indicating whether the planning and execution was successful.
        success = self.move_group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement
        self.move_group.stop()
        # It is always good to clear your targets after planning with poses.
        # Note: there is no equivalent function for clear_joint_value_targets().
        self.move_group.clear_pose_targets()

        ## END_SUB_TUTORIAL

        # For testing:
        # Note that since this section of code will not be included in the tutorials
        # we use the class variable rather than the copied state variable
        current_pose = self.move_group.get_current_pose().pose
        return all_close(pose_goal, current_pose, 0.01)

def main():
    try:
        bot = Robot()
        inp = '1'
        while not rospy.is_shutdown():
            # inp = input(f"{Fore.CYAN}Enter\n- '1' to oscilate\nValue:")
            if int(inp) == 1:
                bot.oscillate()
                continue
            else:
                continue

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
