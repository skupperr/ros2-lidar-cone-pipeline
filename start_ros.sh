#!/bin/bash

# source ROS2 and workspace 
source /opt/ros/humble/setup.bash
source /workspace/ros2_ws/install/setup.bash

echo "Starting ROS2 Sensor System..."

# Run the subscriber and publisher 
ros2 run lidar_pipeline lidar_simulator &
ros2 run lidar_pipeline point_filter &
ros2 run lidar_pipeline cone_detector &
ros2 run lidar_pipeline decision_node

# keep the container running
wait