#!/usr/bin/env python3

import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle
from functools import partial


class TurtleControllerNode(Node):

    def __init__(self):
        super().__init__("turtle_controller")

        # parameter
        self.declare_parameter("catch_closest_turtle_first", True)
        self.catch_closest_turtle_first_ = self.get_parameter(
            "catch_closest_turtle_first"
        ).value

        self.pose_ = None
        self.turtle_to_catch_ = None
        self.catching_in_progress_ = False

        # publisher
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist,
            "/turtle1/cmd_vel",
            10
        )

        # subscribers
        self.pose_subscriber_ = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.callback_pose,
            10
        )

        self.alive_turtles_subscriber_ = self.create_subscription(
            TurtleArray,
            "alive_turtles",
            self.callback_alive_turtles,
            10
        )

        # service client
        self.catch_turtle_client_ = self.create_client(
            CatchTurtle,
            "catch_turtle"
        )

        self.get_logger().info("Waiting for catch_turtle service...")
        self.catch_turtle_client_.wait_for_service()
        self.get_logger().info("Service available!")

        # timer
        self.control_loop_timer_ = self.create_timer(
            0.01,
            self.control_loop
        )

    def callback_pose(self, pose: Pose):
        self.pose_ = pose

    def callback_alive_turtles(self, msg: TurtleArray):
        if len(msg.turtles) == 0:
            self.turtle_to_catch_ = None
            return

        # Prevent crash if pose not received yet
        if self.pose_ is None:
            return

        if self.catch_closest_turtle_first_:
            closest_turtle = None
            closest_distance = float("inf")

            for turtle in msg.turtles:
                dist_x = turtle.x - self.pose_.x
                dist_y = turtle.y - self.pose_.y
                distance = math.sqrt(dist_x**2 + dist_y**2)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_turtle = turtle

            self.turtle_to_catch_ = closest_turtle

        else:
            self.turtle_to_catch_ = msg.turtles[0]

    def control_loop(self):
        if self.pose_ is None or self.turtle_to_catch_ is None:
            return

        dist_x = self.turtle_to_catch_.x - self.pose_.x
        dist_y = self.turtle_to_catch_.y - self.pose_.y
        distance = math.sqrt(dist_x**2 + dist_y**2)

        cmd = Twist()

        if distance > 0.2:
            goal_theta = math.atan2(dist_y, dist_x)
            diff = goal_theta - self.pose_.theta

            # normalize angle
            diff = math.atan2(
                math.sin(diff),
                math.cos(diff)
            )

            if abs(diff) > 0.2:
                cmd.linear.x = 0.0
            else:
                cmd.linear.x = min(2.5 * distance, 4.0)

            cmd.angular.z = 6.0 * diff

        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

            # avoid multiple service calls
            if not self.catching_in_progress_:
                self.catching_in_progress_ = True
                self.call_catch_turtle_service(
                    self.turtle_to_catch_.name
                )

        self.cmd_vel_publisher_.publish(cmd)

    def call_catch_turtle_service(self, turtle_name):
        request = CatchTurtle.Request()
        request.name = turtle_name

        future = self.catch_turtle_client_.call_async(request)

        future.add_done_callback(
            partial(
                self.callback_catch_response,
                turtle_name=turtle_name
            )
        )

    def callback_catch_response(self, future, turtle_name):
        try:
            response = future.result()

            if response.success:
                self.get_logger().info(
                    f"Turtle {turtle_name} caught!"
                )
            else:
                self.get_logger().error(
                    f"Could not catch {turtle_name}"
                )

        except Exception as e:
            self.get_logger().error(
                f"Service call failed: {e}"
            )

        finally:
            self.turtle_to_catch_ = None
            self.catching_in_progress_ = False


def main(args=None):
    rclpy.init(args=args)

    node = TurtleControllerNode()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()