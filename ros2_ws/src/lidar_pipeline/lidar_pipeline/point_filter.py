import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class PointFilter(Node):

    def __init__(self):
        super().__init__('point_filter')

        self.subscription = self.create_subscription(
            Float32MultiArray,
            'lidar_points',
            self.listener_callback,
            10
        )

        self.publisher = self.create_publisher(
            Float32MultiArray,
            'filtered_points',
            10
        )

    def listener_callback(self, msg):

        raw_points = msg.data

        filtered_points = []

        for i in range(0, len(raw_points), 2):

            x = raw_points[i]
            y = raw_points[i+1]

            distance = (x**2 + y**2) ** 0.5

            if distance < 8.0:
                filtered_points.extend([x, y])

        output_msg = Float32MultiArray()
        output_msg.data = filtered_points

        self.publisher.publish(output_msg)

        self.get_logger().info(
            f"Filtered {len(raw_points)//2} → {len(filtered_points)//2} points"
        )


def main(args=None):

    rclpy.init(args=args)

    node = PointFilter()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()