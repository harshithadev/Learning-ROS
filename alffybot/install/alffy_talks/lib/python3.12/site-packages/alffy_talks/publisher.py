import rclpy
from rclpy.node import Node 
from std_msgs.msg import String

class Publisher(Node):
    def __init__(self):
        super().__init__("publisher")
        self.pub_ = self.create_publisher(String, "Emergency", 10)
        self.freqency_ = 20.0
        self.counter = 0
        self.timer = self.create_timer(self.freqency_, self.callBack)
    
    def callBack(self):
        msg = String()
        msg.data = "Alert no : %d" % self.counter
        self.counter += 1
        
        self.pub_.publish(msg)

def main():
    rclpy.init()
    
    publisher = Publisher()
    rclpy.spin(publisher)
    publisher.destroy_node()
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()      