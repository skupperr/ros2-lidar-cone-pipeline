import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import random


class LidarSimulator(Node):

    def __init__(self):
        super().__init__('lidar_simulator')

        self.publisher = self.create_publisher(
            Float32MultiArray,
            'lidar_points',
            10
        )
        [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2]

        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.publish_points)

    def publish_points(self):

        msg = Float32MultiArray()

        points = []

        # Generate random background points
        for _ in range(40):
            x = random.uniform(0, 10)
            y = random.uniform(-5, 5)
            points.extend([x, y])

        # Simulate a cone cluster
        cone_x = random.uniform(2, 8)
        cone_y = random.uniform(-2, 2)

        for _ in range(10):
            x = cone_x + random.uniform(-0.2, 0.2)
            y = cone_y + random.uniform(-0.2, 0.2)
            points.extend([x, y])

        msg.data = points

        self.publisher.publish(msg)

        self.get_logger().info(f'Generated {len(points)//2} lidar points')



def main(args=None):

    rclpy.init(args=args)

    node = LidarSimulator()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()