import rclpy 
from rclpy.node import Node  
from std_msgs.msg import String 

class Subscriber(Node): 
    def __init__(self): 
        super().__init__("subscriber") 
        self.sub_ = self.create_subscription(String, "Emergency", self.msgCallback, 10) 
    
    def msgCallback(self, msg): 
        self.get_logger().info("I captured this msg : %s " % msg.data) 

def main(): 

    rclpy.init() 
    sub = Subscriber() 
    rclpy.spin(sub) 
    sub.destroy_node() 
    rclpy.shutdown() 

if __name__ == "__main__": 
    main() 

 