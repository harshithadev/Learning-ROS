import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/harshdev/Documents/harsh/ROS/bumperbot/install/bumperbot_py'
