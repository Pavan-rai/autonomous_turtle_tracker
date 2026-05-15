#!/usr/bin/env python3

import rclpy
import random
import math
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from functools import partial
from my_robot_interfaces.msg import Turtle, TurtleArray
from my_robot_interfaces.srv import CatchTurtle


class TurtleSpawnerNode(Node):

    def __init__(self):
        super().__init__("turtle_spawner")

        # Parameters
        self.declare_parameter("turtle_name_prefix", "turtle")
        self.declare_parameter("spawn_frequency", 1.0)
        self.declare_parameter("max_turtles", 5)

        self.turtle_name_prefix_ = self.get_parameter(
            "turtle_name_prefix"
        ).value

        self.spawn_frequency_ = self.get_parameter(
            "spawn_frequency"
        ).value

        self.max_turtles_ = self.get_parameter(
            "max_turtles"
        ).value

        # Prevent divide by zero
        if self.spawn_frequency_ <= 0:
            self.get_logger().warn(
                "spawn_frequency must be > 0. Using default value 1.0"
            )
            self.spawn_frequency_ = 1.0

        self.turtle_counter_ = 0
        self.alive_turtles_ = []

        # Publisher
        self.alive_turtles_publisher_ = self.create_publisher(
            TurtleArray,
            "alive_turtles",
            10
        )

        # Service
        self.catch_turtle_service_ = self.create_service(
            CatchTurtle,
            "catch_turtle",
            self.callback_catch_turtle
        )

        # Clients
        self.spawn_client_ = self.create_client(
            Spawn,
            "/spawn"
        )

        self.kill_client_ = self.create_client(
            Kill,
            "/kill"
        )

        self.get_logger().info("Waiting for services...")
        self.spawn_client_.wait_for_service()
        self.kill_client_.wait_for_service()
        self.get_logger().info("Services ready!")

        # Timer
        self.spawn_turtle_timer_ = self.create_timer(
            1.0 / self.spawn_frequency_,
            self.spawn_new_turtle
        )

    def callback_catch_turtle(self, request, response):
        self.call_kill_service(request.name)
        response.success = True
        return response

    def publish_alive_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.alive_turtles_publisher_.publish(msg)

    def spawn_new_turtle(self):
        # Prevent too many turtles
        if len(self.alive_turtles_) >= self.max_turtles_:
            return

        self.turtle_counter_ += 1
        name = f"{self.turtle_name_prefix_}{self.turtle_counter_}"

        x = random.uniform(1.0, 10.0)
        y = random.uniform(1.0, 10.0)
        theta = random.uniform(0.0, 2 * math.pi)

        self.call_spawn_service(name, x, y, theta)

    def call_spawn_service(self, turtle_name, x, y, theta):
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name

        future = self.spawn_client_.call_async(request)

        future.add_done_callback(
            partial(
                self.callback_spawn_response,
                request=request
            )
        )

    def callback_spawn_response(self, future, request):
        try:
            response = future.result()

            if response.name:
                self.get_logger().info(
                    f"Spawned: {response.name}"
                )

                new_turtle = Turtle()
                new_turtle.name = response.name
                new_turtle.x = request.x
                new_turtle.y = request.y
                new_turtle.theta = request.theta

                self.alive_turtles_.append(new_turtle)
                self.publish_alive_turtles()

        except Exception as e:
            self.get_logger().error(
                f"Spawn failed: {e}"
            )

    def call_kill_service(self, turtle_name):
        request = Kill.Request()
        request.name = turtle_name

        future = self.kill_client_.call_async(request)

        future.add_done_callback(
            partial(
                self.callback_kill_response,
                turtle_name=turtle_name
            )
        )

    def callback_kill_response(self, future, turtle_name):
        try:
            future.result()

            self.get_logger().info(
                f"Killed: {turtle_name}"
            )

            self.alive_turtles_ = [
                t for t in self.alive_turtles_
                if t.name != turtle_name
            ]

            self.publish_alive_turtles()

        except Exception as e:
            self.get_logger().error(
                f"Kill failed: {e}"
            )


def main(args=None):
    rclpy.init(args=args)

    node = TurtleSpawnerNode()

    # optional starter turtle
    node.call_spawn_service(
        "test",
        3.0,
        3.0,
        0.0
    )

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()