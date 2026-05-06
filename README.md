# ROS2 LiDAR Cone Detection Pipeline

## Overview

This project implements a **simplified LiDAR perception pipeline using ROS2** designed to simulate how autonomous vehicles detect cones on a race track.

The system simulates LiDAR point clouds, processes them through multiple perception stages, and outputs a driving decision based on detected cones.

The entire system is **containerized using Docker**, meaning **ROS2 does not need to be installed on the host machine**.

Once the repository is cloned, the entire pipeline can be executed using a single command.

---

# System Architecture

The ROS2 system consists of multiple nodes that form a **perception pipeline**.

```
LiDAR Simulator
      │
      │  Topic: /lidar_points
      ▼
Point Filter
      │
      │  Topic: /filtered_points
      ▼
Cone Detector
      │
      │  Topic: /cone_centers
      ▼
Decision Node
```

Each node performs a specific task in the perception stack.

---

# Pipeline Description

## 1. LiDAR Simulator Node

This node simulates a **2D LiDAR scan**.

It generates:

* **Background points** representing environmental noise
* **Clusters of points** representing traffic cones

Each scan is published as a **list of (x, y) coordinates**.

### Output Topic

```
/lidar_points
```

### Message Type

```
std_msgs/msg/Float32MultiArray
```

Example representation:

```
[x1, y1, x2, y2, x3, y3 ...]
```

Each pair represents one point in the LiDAR scan.

---

## 2. Point Filter Node

The filter removes points that are outside the region of interest.

The distance of each point from the LiDAR origin is calculated using:

d = sqrt(x² + y²)

Only points within a specified distance range are kept.

### Purpose

This simulates **preprocessing performed in real perception pipelines** where far-away or irrelevant points are discarded before clustering.

### Output Topic

```
/filtered_points
```

---

## 3. Cone Detector Node

The cone detector identifies clusters of LiDAR points that represent cones.

The algorithm:

1. Iterates through filtered points
2. Groups nearby points into clusters
3. Calculates the **centroid of each cluster**

Cluster center is calculated using:

x_center = (1/N) * Σ xi

y_center = (1/N) * Σ yi

Each cluster center represents a **detected cone location**.

### Output Topic

```
/cone_centers
```

Example:

```
Detected 2 cones
Detected 1 cones
```

---

## 4. Decision Node

The decision node analyzes detected cone positions and produces a simple driving command.

Example logic:

| Condition           | Decision    |
| ------------------- | ----------- |
| Minimum distance < 2.0  | STOP |
| Minimum distance < 5.0 | SLOW DOWN  |
| No cone ahead       | CLEAR |

Example output:

```
Nearest cone: 4.188245872916913 → Decision: SLOW_DOWN
```

This simulates the **decision layer of an autonomous driving stack**.

---

# Example Output

Example terminal output when the system runs:

```
[lidar_simulator]: Generated 50 lidar points
[point_filter]: Filtered 50 → 42 points
[cone_detector]: Detected 2 cones
[decision_node]: Nearest cone: 4.188245872916913 → Decision: SLOW_DOWN

```

---

# Project Structure

```
ros2-lidar-cone-pipeline
│
├── Dockerfile
├── start_ros.sh
├── run.sh
├── README.md
│
└── ros2_ws
    └── src
        └── lidar_pipeline
            ├── package.xml
            ├── setup.cfg
            ├── setup.py
            └── lidar_pipeline
                ├── __init__.py
                ├── lidar_simulator.py
                ├── point_filter.py
                ├── cone_detector.py
                └── decision_node.py
```

### Important Files

| File               | Description                                          |
| ------------------ | ---------------------------------------------------- |
| Dockerfile         | Builds the ROS2 container and compiles the workspace |
| start_ros.sh       | Launches the ROS2 pipeline inside the container      |
| run.sh             | Helper script to build and run the system            |
| lidar_simulator.py | Simulates LiDAR scans                                |
| point_filter.py    | Removes irrelevant points                            |
| cone_detector.py   | Detects clusters representing cones                  |
| decision_node.py   | Generates driving decisions                          |

---

# Prerequisites

You only need:

* **Docker**

Install Docker:

[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

Verify installation:

```bash
docker --version
```

Example:

```
Docker version 24.x.x
```

---

# Running the Project

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/ros2-lidar-cone-pipeline.git
```

Navigate to the project directory:

```bash
cd ros2-lidar-cone-pipeline
```

---

## 2. Run the System

Execute the helper script:

```bash
./run.sh
```

This script will automatically:

1. Build the Docker image
2. Start the container
3. Launch the ROS2 pipeline

---

# Expected Output

Example output:

```
Building Docker image: ros2_lidar_simulation
[+] Building 1.1s (12/12) FINISHED    
Running Docker container from image: ros2_lidar_simulation
Starting ROS2 Sensor System...
Generated 50 lidar points
Filtered 50 → 38 points
Detected 1 cones
Nearest cone: 6.9807022413710795 → Decision: CLEAR

```

---

# What the Helper Script Does

The script `run.sh` performs two main actions.

### Build the Docker Image

```
docker build -t ros_lidar_pipeline .
```

### Run the Container

```
docker run --rm ros_lidar_pipeline
```

The `--rm` flag ensures the container is removed when it exits.

---

# Running Manually (Optional)

If you want to run commands manually instead of using the script:

### Build Image

```bash
docker build -t ros_lidar_pipeline .
```

### Run Container

```bash
docker run ros_lidar_pipeline
```

---

# How the Docker Container Works

The container uses the official **ROS2 Humble base image**.

Inside the container:

### Load ROS2 environment

```
source /opt/ros/humble/setup.bash
```

### Load workspace

```
source /workspace/ros2_ws/install/setup.bash
```

### Start the pipeline

```
ros2 run lidar_pipeline lidar_simulator
ros2 run lidar_pipeline point_filter
ros2 run lidar_pipeline cone_detector
ros2 run lidar_pipeline decision_node
```

Each node communicates through ROS topics.

---

# ROS Concepts Used

## Node

A **node** is an executable component of a ROS system.

Nodes in this project:

```
lidar_simulator
point_filter
cone_detector
decision_node
```

---

## Topic

Nodes communicate using **topics**.

Examples:

```
/lidar_points
/filtered_points
/cone_centers
```

---

## Message Types

The pipeline uses:

```
std_msgs/msg/Float32MultiArray
```

This allows transmitting arrays representing LiDAR points.

---

# Technologies Used

| Technology  | Purpose               |
| ----------- | --------------------- |
| ROS2 Humble | Robotics middleware   |
| Python      | ROS2 node development |
| Docker      | Containerization      |
| colcon      | ROS build system      |

---

<!-- # Future Improvements

Possible improvements to make the pipeline closer to a real autonomous system:

* Visualization using **RViz**
* Use real **sensor_msgs/PointCloud2** messages
* Implement **DBSCAN clustering**
* Add **cone classification**
* Integrate with a **path planning module** -->

<!-- --- -->
