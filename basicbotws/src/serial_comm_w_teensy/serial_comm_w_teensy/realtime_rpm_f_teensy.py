import rclpy
from rclpy.node import Node
import serial
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')

        # Initialize serial connection
        self.serial_port = '/dev/ttyACM0'
        self.baud_rate = 115200
        self.connect_serial()

        # Publisher for motor RPM feedback
        self.rpm_publisher = self.create_publisher(String, '/motor_rpm', 10)

        # Subscriber for cmd_vel
        self.cmd_vel_subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)

        # Timer to read motor feedback
        self.timer = self.create_timer(0.1, self.read_serial)

        # Robot Parameters
        self.wheel_radius = 0.075  # 7.5 cm (0.075 m)
        self.wheel_separation = 0.5  # 50 cm (0.5 m)

        # Initial velocities
        self.linear_x = 0.0
        self.angular_z = 0.0

    def connect_serial(self):
        """Try to establish a serial connection, handle disconnections and reboots."""
        while True:
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=2)
                self.get_logger().info(f"Connected to Teensy on {self.serial_port}")
                time.sleep(2)  # Wait for Teensy to fully reboot
                return
            except serial.SerialException:
                self.get_logger().error(f"Teensy not found on {self.serial_port}, retrying...")
                time.sleep(2)  # Wait before retrying

    def cmd_vel_callback(self, msg):
        """Callback function to handle incoming velocity commands."""
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z
        self.send_velocity_as_rpm()

    def velocity_to_rpm(self, linear_x, angular_z):
        """Convert linear and angular velocity to wheel RPM"""
        left_wheel_speed = (linear_x - (angular_z * (self.wheel_separation / 2))) / self.wheel_radius
        right_wheel_speed = (linear_x + (angular_z * (self.wheel_separation / 2))) / self.wheel_radius

        left_rpm = (left_wheel_speed * 60) / (2 * 3.1416)  # Convert rad/s to RPM
        right_rpm = (right_wheel_speed * 60) / (2 * 3.1416)

        return int(left_rpm), int(right_rpm)

    def send_velocity_as_rpm(self):
        """Convert velocity to RPM and send to Teensy."""
        left_rpm, right_rpm = self.velocity_to_rpm(self.linear_x, self.angular_z)

        command = f"SETPOINT {left_rpm} {right_rpm}\n"
        try:
            self.ser.write(command.encode())
            self.get_logger().info(f"Sent: {command.strip()}")
        except serial.SerialException:
            self.get_logger().error("Failed to send RPM, attempting to reconnect...")
            self.reconnect_serial()

    def read_serial(self):
        """Read RPM feedback from Teensy and publish it in ROS2."""
        try:
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode().strip()
                if response.startswith("RPM"):
                    self.rpm_publisher.publish(String(data=response))
                    self.get_logger().info(f"Teensy: {response}")
        except serial.SerialException:
            self.get_logger().error("Serial connection lost, attempting to reconnect...")
            self.reconnect_serial()
        except OSError:
            self.get_logger().error("OSError: Teensy may have rebooted, reconnecting...")
            self.reconnect_serial()

    def reconnect_serial(self):
        """Close the serial connection and attempt to reconnect."""
        self.get_logger().info("Closing serial connection...")
        self.ser.close()
        time.sleep(2)

        while True:
            try:
                self.get_logger().info("Attempting to reconnect...")
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=2)
                self.get_logger().info(f"Reconnected to Teensy on {self.serial_port}")
                time.sleep(2)  # Wait for Teensy to initialize
                return
            except serial.SerialException as e:
                self.get_logger().error(f"Reconnection failed: {e}, retrying in 2s...")
                time.sleep(2)


def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#  Use the below mentioned command to publish to said topic (for testing)
# ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}"
