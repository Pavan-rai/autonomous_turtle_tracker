# ROS2 Autonomous Target Tracking (Turtlesim Catch Them All)

A ROS2-based autonomous turtle tracking system where a controller turtle detects, chases, and catches spawned turtles inside `turtlesim`.

This project demonstrates:

- ROS2 Publishers/Subscribers
- Custom Messages
- Custom Services
- Launch Files
- YAML Parameter Configuration
- Autonomous Motion Control
- Multi-node Communication
- Async Service Calls

---

## Demo

Main turtle automatically:

- Detects spawned turtles
- Chooses nearest target
- Navigates toward target
- Removes target after catching it
- Continues until all turtles are removed

---

## Project Architecture

### Nodes

### 1. `turtle_spawner`
Responsible for:

- Spawning new turtles
- Publishing alive turtles list
- Killing turtles when requested

### 2. `turtle_controller`
Responsible for:

- Subscribing to turtle positions
- Selecting nearest turtle
- Moving toward target
- Calling catch service

---

## Custom Interfaces

### `Turtle.msg`

```text
string name
float64 x
float64 y
float64 theta
```

---

### `TurtleArray.msg`

```text
my_robot_interfaces/msg/Turtle[] turtles
```

---

### `CatchTurtle.srv`

```text
string name
---
bool success
```

---

## Technologies Used

- ROS2 Humble
- Python
- Turtlesim
- Custom ROS Interfaces
- YAML
- Git/GitHub

---

## Project Structure

```bash
ros2_ws/
│
├── src/
│   ├── my_robot_interfaces/
│   ├── turtlesim_catch_them_all/
│   └── my_robot_bringup/
│
├── build/
├── install/
└── log/
```

---

## Features

- Dynamic turtle spawning
- Nearest turtle tracking
- Configurable spawn frequency
- Custom turtle naming
- YAML-based parameter tuning
- Launch file automation

---

## Parameter Configuration

Example:

```yaml
/turtle_controller:
  ros__parameters:
    catch_closest_turtle_first: true

/turtle_spawner:
  ros__parameters:
    turtle_name_prefix: "my_turtle"
    spawn_frequency: 1.5
```

---

## Run Project

### Build workspace

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

### Launch project

```bash
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml
```

---

## ROS Concepts Demonstrated

- Publisher/Subscriber communication
- Service communication
- Custom interfaces
- Motion planning basics
- Parameter server usage
- Multi-node robotics systems

---

## Future Improvements

- Path optimization
- Obstacle avoidance
- Gazebo integration
- TurtleBot implementation
- Computer vision target detection
- Reinforcement learning for navigation

---

## Why This Project?

This project was built to strengthen practical understanding of ROS2 architecture and autonomous robotics systems.

It simulates real-world robotics concepts like:

- Target tracking
- Autonomous navigation
- Distributed node communication
- Robot decision-making

---

## Author

**Pavan Rai**

GitHub: https://github.com/pavan123437
