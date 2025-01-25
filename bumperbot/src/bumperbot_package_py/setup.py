from setuptools import find_packages, setup

package_name = 'bumperbot_package_py'

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
    maintainer_email='harshdev@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher = bumperbot_package_py.publisher:main',
            'subscriber = bumperbot_package_py.subscriber:main',
            'parameters = bumperbot_package_py.parameters:main', 
        ],
    },
)
