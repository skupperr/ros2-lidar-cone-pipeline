import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import math


class ConeDetector(Node):

    def __init__(self):
        super().__init__('cone_detector')

        self.subscription = self.create_subscription(
            Float32MultiArray,
            'filtered_points',
            self.callback,
            10
        )

        self.publisher = self.create_publisher(
            Float32MultiArray,
            'detected_cones',
            10
        )

    def callback(self, msg):

        points = msg.data

        cones = []

        visited = set()

        for i in range(0, len(points), 2):

            if i in visited:
                continue

            cluster_x = []
            cluster_y = []

            base_x = points[i]
            base_y = points[i + 1]

            visited.add(i)

            cluster_x.append(base_x)
            cluster_y.append(base_y)

            # simple clustering (threshold-based)
            for j in range(i + 2, len(points), 2):

                if j in visited:
                    continue

                x = points[j]
                y = points[j + 1]

                dist = math.sqrt((base_x - x)**2 + (base_y - y)**2)

                if dist < 0.5:
                    visited.add(j)
                    cluster_x.append(x)
                    cluster_y.append(y)

            if len(cluster_x) >= 3:

                cx = sum(cluster_x) / len(cluster_x)
                cy = sum(cluster_y) / len(cluster_y)

                cones.extend([cx, cy])

        output = Float32MultiArray()
        output.data = cones

        self.publisher.publish(output)

        self.get_logger().info(
            f"Detected {len(cones)//2} cones"
        )


def main(args=None):

    rclpy.init(args=args)

    node = ConeDetector()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()