import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/harshdev/Learning-ROS/basicbotws/install/joy_to_cmd_vel'
