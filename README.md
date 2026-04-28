# ROS2 Sensor Simulator

## Overview

This project implements a simple **sensor simulation system using ROS2**. It consists of two nodes:

* **Publisher Node** - simulates a sensor by generating temperature values.
* **Subscriber Node** - listens to the sensor data and prints warnings if values exceed a threshold.

The system is fully containerized using **Docker**, meaning **ROS2 does not need to be installed on the host machine**.

Once the project is cloned, the entire system can be run with a single command.

---

# System Architecture

The ROS2 system consists of two nodes communicating through a topic.

```
Sensor Publisher Node
        │
        │  Topic: /sensor_data
        v
Sensor Subscriber Node
```

### Publisher

* Generates random temperature values between **20°C and 30°C**
* Publishes data every **1 second**

### Subscriber

* Subscribes to `/sensor_data`
* Prints received values
* Triggers a warning when temperature exceeds **28°C**

Example output:

```
Publishing: 23.44
Received sensor value: 23.44

Publishing: 29.10
Received sensor value: 29.10
WARNING: Temperature too high!
```

---

# Project Structure

```
ros2-sensor-simulator
│
├── Dockerfile
├── start_ros.sh
├── run.sh
├── README.md
│
└── ros2_ws
    └── src
        └── sensor_simulator
            ├── package.xml
            ├── setup.py
            └── sensor_simulator
                ├── __init__.py
                ├── sensor_publisher.py
                └── sensor_subscriber.py
```

### Important Files

| File                   | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `Dockerfile`           | Builds the ROS2 container and compiles the workspace |
| `start_ros.sh`         | Starts the ROS nodes inside the container            |
| `run.sh`               | Helper script to build and run the system            |
| `sensor_publisher.py`  | Simulated sensor node                                |
| `sensor_subscriber.py` | Data processing node                                 |

---

# Prerequisites

You only need:

* **Docker**

Install Docker from:

[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

Verify installation:

```bash
docker --version
```

Example output:

```
Docker version 24.x.x
```

---

# Running the Project

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/ros2-sensor-simulator.git
```

Navigate to the project:

```bash
cd ros2-sensor-simulator
```

---

## 2. Run the System

Execute the helper script:

```bash
./run.sh
```

This script will:

1. Build the Docker image
2. Start the container
3. Launch the ROS2 nodes

---

## 3. Expected Output

Example logs:

```
Building Docker image...
Successfully built ...

Running ROS2 sensor simulation...

Starting ROS2 Sensor System...

Publishing: 23.55
Received sensor value: 23.55

Publishing: 28.94
Received sensor value: 28.94
WARNING: Temperature too high!
```

The publisher and subscriber are now communicating via ROS2 topics.

---

# What the Helper Script Does

The script `run.sh` performs two actions:

### Build the Docker Image

```
docker build -t ros_sensor_sim .
```

### Run the Container

```
docker run --rm ros_sensor_sim
```

The `--rm` flag ensures the container is removed after it stops.

---

# Running the Container Manually (Optional)

If you want to run the commands manually instead of using the script:

### Build Image

```bash
docker build -t ros_sensor_sim .
```

### Run Container

```bash
docker run ros_sensor_sim
```

---

# How the Docker Container Works

The container uses the official **ROS2 Humble base image**.

Inside the container the following steps occur:

1. ROS2 environment is loaded

```
source /opt/ros/humble/setup.bash
```

2. The ROS workspace environment is sourced

```
source /workspace/ros2_ws/install/setup.bash
```

3. ROS nodes are launched

```
ros2 run sensor_simulator sensor_subscriber
ros2 run sensor_simulator sensor_publisher
```

The subscriber is started first so it can immediately receive messages.

---

# ROS Concepts Used

### Node

A node is an executable program that participates in the ROS network.

Example nodes in this project:

```
sensor_publisher
sensor_subscriber
```

---

### Topic

Nodes communicate through **topics**.

Publisher sends messages to:

```
/sensor_data
```

Subscriber listens to the same topic.

---

### Message Type

The topic uses the standard ROS message:

```
std_msgs/msg/Float32
```

This allows sending numeric values representing temperature.

---

# Technologies Used

| Technology     | Purpose                    |
| -------------- | -------------------------- |
| ROS2 Humble    | Robotics middleware        |
| Python         | ROS2 Python client library |
| Docker         | Containerization           |
| colcon         | ROS build system           |

---