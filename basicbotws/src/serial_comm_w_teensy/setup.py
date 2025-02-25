from setuptools import find_packages, setup

package_name = 'serial_comm_w_teensy'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='harshdev',
    maintainer_email='harshithadevineni16@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'serial_comm_w_teensy = serial_comm_w_teensy.serial_comm_w_teensy:main', 
            'realtime_rpm_f_teensy = serial_comm_w_teensy.realtime_rpm_f_teensy:main',
        ],
    },
)
