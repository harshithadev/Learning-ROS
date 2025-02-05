import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class PointToPointNav(Node):
    def __init__(self):
        super().__init__('point_to_point_nav')
        
        # Publisher for velocity commands
        self.vel_pub = self.create_publisher(Twist, '/diff_cont/cmd_vel_unstamped', 10)
        
        # Subscriber to odometry
        self.odom_sub = self.create_subscription(Odometry, '/diff_cont/odom', self.odom_callback, 10)
        # Goal coordinates (Change these as needed)
        self.goal_x = 2.0  # Set your target X position
        self.goal_y = 2.0  # Set your target Y position

        # Robot's current position
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

        # Control parameters
        self.linear_speed = 0.2
        self.angular_speed = 0.5
        self.tolerance = 0.1  # Stop when within this distance of the goal

    def odom_callback(self, msg):

        # Extract position
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
 
        # Extract orientation (quaternion to yaw)
        q = msg.pose.pose.orientation
        self.current_yaw = self.quaternion_to_yaw(q)
 
        # Move towards the goal
        self.navigate_to_goal()
 
    def quaternion_to_yaw(self, q):
        """Convert quaternion to yaw angle."""
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)
 
    def navigate_to_goal(self):
        """Compute movement commands and send to robot."""
        dx = self.goal_x - self.current_x
        dy = self.goal_y - self.current_y

        distance = math.sqrt(dx**2 + dy**2)
        goal_angle = math.atan2(dy, dx)
        angle_error = goal_angle - self.current_yaw

        cmd = Twist() 
        if distance > self.tolerance:
            # Rotate towards the goal
            if abs(angle_error) > 0.1:
                cmd.angular.z = self.angular_speed * (angle_error / abs(angle_error))  # Normalize direction
            else:
                cmd.linear.x = self.linear_speed  # Move forward

        self.vel_pub.publish(cmd) 
        # Stop when close enough
        if distance <= self.tolerance:
            self.get_logger().info("Goal reached!")
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.vel_pub.publish(cmd)
 
def main(args=None):
    rclpy.init(args=args)
    node = PointToPointNav()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

 