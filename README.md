# 🐢 ROS2 Autonomous Target Tracking — Turtlesim Catch Them All


A ROS2-based autonomous turtle tracking system where a controller turtle intelligently detects, pursues, and catches dynamically spawned turtles inside `turtlesim`.

The project demonstrates real-world robotics concepts such as autonomous navigation, ROS2 communication, custom interfaces, services, and multi-node robotic architecture.

---

# 🎥 Demo

## Project Video

[Uploading Screencast from 05-15-2026 08:52:22 PM.webm…]()


### Autonomous behavior

✅ Detect spawned turtles  
✅ Track nearest target  
✅ Navigate autonomously  
✅ Catch and remove turtles  
✅ Continue until all turtles are eliminated  

---

# ✨ Features

- Dynamic turtle spawning
- Nearest target selection algorithm
- Autonomous target pursuit
- Async service communication
- YAML configurable parameters
- Custom ROS messages and services
- Multi-node architecture
- Launch file automation
- Modular ROS2 package design

---

# 🏗 System Architecture

```text
                +------------------+
                | turtle_spawner   |
                +------------------+
                         |
                         | publishes
                         ↓

                +------------------+
                | Alive Turtles    |
                | TurtleArray.msg  |
                +------------------+
                         |
                         ↓ subscribes

                +------------------+
                | turtle_controller|
                +------------------+
                         |
                  computes target
                         ↓

                 Velocity Commands
                         ↓

                 Controller Turtle
                         ↓

                    Catch Service
```

---

# 🔧 Nodes

## 1️⃣ turtle_spawner

Responsibilities:

- Spawn turtles dynamically
- Publish alive turtles list
- Handle turtle removal requests
- Manage turtle lifecycle

---

## 2️⃣ turtle_controller

Responsibilities:

- Subscribe to turtle positions
- Select nearest turtle
- Compute movement commands
- Move toward target
- Call catch service asynchronously

---

# 📦 Custom Interfaces

## Turtle.msg

```text
string name
float64 x
float64 y
float64 theta
```

---

## TurtleArray.msg

```text
Turtle[] turtles
```

---

## CatchTurtle.srv

```text
string name
---
bool success
```

---

# ⚙ Technologies Used

- ROS2 Humble
- Python
- Turtlesim
- YAML
- Custom ROS Interfaces
- Git + GitHub

---

# 📂 Project Structure

```bash
autonomous_turtle_tracker/
│
├── my_robot_interfaces/
│   ├── msg/
│   │   ├── Turtle.msg
│   │   └── TurtleArray.msg
│   │
│   └── srv/
│       └── CatchTurtle.srv
│
├── turtlesim_catch_them_all/
│   ├── launch/
│   ├── config/
│   ├── scripts/
│   └── package.xml
│
├── my_robot_bringup/
│
└── README.md
```

---

# ⚙ Parameter Configuration

Example:

```yaml
/ turtle_controller:
  ros__parameters:
    catch_closest_turtle_first: true

/ turtle_spawner:
  ros__parameters:
    turtle_name_prefix: "my_turtle"
    spawn_frequency: 1.5
```

Parameters can be modified without changing source code.

---

# 🚀 Installation

Clone repository:

```bash
git clone https://github.com/Pavan-rai/autonomous_turtle_tracker.git

cd autonomous_turtle_tracker
```

Build workspace:

```bash
colcon build
```

Source setup:

```bash
source install/setup.bash
```

---

# ▶ Run Project

Launch complete system:

```bash
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml
```

---

# 🧠 Workflow

1. Spawn turtles dynamically  
2. Publish alive turtle list  
3. Controller subscribes  
4. Find nearest target  
5. Compute velocity commands  
6. Move toward target  
7. Call catch service  
8. Remove turtle  
9. Repeat until all turtles are caught  

---

# 📚 ROS2 Concepts Demonstrated

- Publisher / Subscriber communication
- Services and async calls
- Custom interfaces
- YAML parameters
- Launch files
- Multi-node systems
- Autonomous decision making

---

# 🔮 Future Improvements

- PID motion controller
- Path optimization
- Obstacle avoidance
- Gazebo integration
- TurtleBot deployment
- Computer vision target detection
- Reinforcement learning navigation

---

# 🎯 Why This Project?

This project was built to strengthen practical understanding of ROS2 architecture and autonomous robotic systems.

It simulates real robotics concepts such as:

- Autonomous navigation
- Target tracking
- Distributed node communication
- Real-time control
- Robot decision-making

---

# 👨‍💻 Author

**Pavan Rai**

GitHub: https://github.com/Pavan-rai

If you found this project useful, consider giving it a ⭐
