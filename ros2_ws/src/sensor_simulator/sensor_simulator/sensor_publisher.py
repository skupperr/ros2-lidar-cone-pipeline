import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class SensorPublisher(Node):

    def __init__(self):
        super().__init__('sensor_publisher')

        self.publisher = self.create_publisher(Float32, 'sensor_data', 10)

        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.publish_sensor_data)

    def publish_sensor_data(self):
        msg = Float32()

        msg.data = random.uniform(20.0, 30.0)

        self.publisher.publish(msg)

        self.get_logger().info(f'Publishing: {msg.data:.2f}')


def main(args=None):

    # initializes the ROS communication system.
    rclpy.init(args=args)

    node = SensorPublisher()

    # starts the ROS event loop. kinda like game loop or socket
    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()