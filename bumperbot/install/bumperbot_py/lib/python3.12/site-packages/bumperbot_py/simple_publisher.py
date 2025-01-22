import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    def __init__(self):
        super().__init__("simple_publisher")
        self.pub_ = self.create_publisher(String, "chatter", 10)

        self.counter_ = 0  # to see how many messages are in the buffer
        self.frequency_ = 1.0 # the number of messages per topic per second 

        self.get_logger().info("Publishing in %d Hz" %self.frequency_)
        self.timer = self.create_timer(self.frequency_, self.timerCallback)

    def timerCallback(self):
        msg = String ()
        msg.data = "this is a message displaced for the %d time" % self.counter_

        self.pub_.publish(msg)
        self.counter_ += 1

def main():
    rclpy.init()

    simplepublisher = SimplePublisher()
    rclpy.spin(simplepublisher)
    simplepublisher.destroy_node()

    rclpy.shutdown()

    
if __name__ == "__main__" :
    main()
    