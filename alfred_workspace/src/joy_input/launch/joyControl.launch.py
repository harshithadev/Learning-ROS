from launch import LaunchDescription
from launch_ros.actions import Node 

joy_node = Node(
   package='joy', 
     executable='joy_node'
)

joy_input = Node (
    package='joy_input', 
    executable='joy_to_cmdvel', 
)

def generate_launch_description():
    return LaunchDescription([
        joy_node, 
        joy_input,
    ])