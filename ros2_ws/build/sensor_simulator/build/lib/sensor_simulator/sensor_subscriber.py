import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SensorSubscriber(Node):

    def __init__(self):
        super().__init__('sensor_subscriber')

        self.subscription = self.create_subscription(
            Float32,
            'sensor_data',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):

        value = msg.data

        self.get_logger().info(f'Received sensor value: {value:.2f}')

        if value > 28.0:
            self.get_logger().warn('WARNING: Temperature too high!')


def main(args=None):

    rclpy.init(args=args)

    node = SensorSubscriber()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()