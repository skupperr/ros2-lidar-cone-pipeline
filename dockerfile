FROM ros:humble-ros-base

WORKDIR /workspace

# workspace is added into the image.
COPY ros2_ws /workspace/ros2_ws
COPY start_ros.sh /workspace/start_ros.sh

# Install colcon and build the workspace.
RUN apt update && apt install -y python3-colcon-common-extensions

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && cd /workspace/ros2_ws && colcon build"

RUN chmod +x /workspace/start_ros.sh

# Start the ROS system automatically when the container is run.
CMD ["/workspace/start_ros.sh"]