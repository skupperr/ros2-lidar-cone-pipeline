#!/bin/bash

# source ROS2 and workspace 
source /opt/ros/humble/setup.bash
source /workspace/ros2_ws/install/setup.bash

echo "Starting ROS2 Sensor System..."

# Run the subscriber and publisher 
ros2 run sensor_simulator sensor_subscriber &
ros2 run sensor_simulator sensor_publisher

# keep the container running
wait