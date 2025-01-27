from rclpy.parameter import Parameter
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class Parameters(Node):
    def __init__(self):
        super().__init__("parameter")
        
        self.declare_parameter("int_param", 10)
        self.declare_parameter("string_param", 'this is a string param')

        self.add_on_set_parameters_callback(self.paramChangeCallback)

    def paramChangeCallback(self, params):
        result = SetParametersResult()
        
        for param in params : 
            if param.name == "int_param" and param.type_ == Parameter.Type.INTEGER:
                self.get_logger().info("Alert ! Value of int_param changed to %d" % param.value)
                result.successful= True
            if param.name == "string_param" and param.type_ == Parameter.Type.STRING:
                self.get_logger().info("Alert ! Value of string_param changed to %s" % param.value)
                result.successful = True
        return result 

def main():
    rclpy.init()
    parameters = Parameters()
    rclpy.spin(parameters)
    parameters.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

