import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
import math


class DecisionNode(Node):

    def __init__(self):
        super().__init__('decision_node')

        self.subscription = self.create_subscription(
            Float32MultiArray,
            'detected_cones',
            self.callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            'decision',
            10
        )

    def callback(self, msg):

        cones = msg.data

        if len(cones) == 0:
            decision = "CLEAR"
        else:
            min_distance = float('inf')

            for i in range(0, len(cones), 2):
                x = cones[i]
                y = cones[i + 1]

                distance = math.sqrt(x**2 + y**2)

                if distance < min_distance:
                    min_distance = distance

            if min_distance < 2.0:
                decision = "STOP"
            elif min_distance < 5.0:
                decision = "SLOW_DOWN"
            else:
                decision = "CLEAR"

        msg_out = String()
        msg_out.data = decision

        self.publisher.publish(msg_out)

        self.get_logger().info(
            f"Nearest cone: {min_distance if cones else 'None'} → Decision: {decision}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = DecisionNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()