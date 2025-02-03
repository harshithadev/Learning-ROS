import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyToCmdVel(Node):
    def __init__(self):
        super().__init__('joy_to_cmd_vel')
        
        # Create a publisher for the /cmd_vel topic
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Create a subscriber to the /joy topic
        self.joy_subscriber = self.create_subscription(
            Joy,
            '/joy',  # Joystick input topic
            self.joy_callback,
            10
        )
    
    def joy_callback(self, msg: Joy):
        # Assuming the left joystick controls linear velocity (x and y) and the right joystick controls angular velocity (z)
        twist_msg = Twist()

        # Map the axes from the joystick to the Twist message
        twist_msg.linear.x = msg.axes[1]  # Forward/backward (left stick vertical)
        twist_msg.linear.y = msg.axes[0]  # Left/right (left stick horizontal)
        twist_msg.angular.z = msg.axes[3]  # Rotation (right stick horizontal)

        # Publish the Twist message to /cmd_vel
        self.cmd_vel_publisher.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = JoyToCmdVel()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
