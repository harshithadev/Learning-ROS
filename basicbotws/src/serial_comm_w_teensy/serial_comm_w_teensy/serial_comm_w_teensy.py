import rclpy
from rclpy.node import Node
import serial
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')

        # Connect to Teensy over USB Serial
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.get_logger().info("Connected to Teensy on /dev/ttyACM0")

        # Subscribe to /cmd_vel (velocity commands from ROS2)
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
        # Publisher for motor feedback (RPM)
        self.rpm_publisher = self.create_publisher(String, '/motor_rpm', 10)

        # Timer to read motor feedback
        self.timer = self.create_timer(0.1, self.read_serial)

    def cmd_vel_callback(self, msg):
        """Convert ROS2 /cmd_vel into a serial command for Teensy"""
        command = f"VEL {msg.linear.x} {msg.angular.z}\n"
        self.ser.write(command.encode())
        self.get_logger().info(f"Sent: {command.strip()}")

    def read_serial(self):
        """Read RPM feedback from Teensy and publish it in ROS2"""
        if self.ser.in_waiting > 0:
            response = self.ser.readline().decode().strip()
            if response.startswith("RPM"):
                self.rpm_publisher.publish(String(data=response))
                self.get_logger().info(f"Teensy: {response}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
