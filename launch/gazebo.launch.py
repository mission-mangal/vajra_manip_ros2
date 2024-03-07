import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    gazebo_launch_file = os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch', 'empty_world.launch.py')
    
    manipulator_urdf = os.path.join(
        get_package_share_directory('kai'), 'urdf', 'manipulator.urdf')
    
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([gazebo_launch_file])
        ),
        ExecuteProcess(
            cmd=[
                'static_transform_publisher', '0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint'
            ],
            name='tf_footprint_base'
        ),
        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'gazebo_ros', 'spawn_entity', '-entity', 'manipulator', '-file', manipulator_urdf
            ],
            name='spawn_model'
        ),
        ExecuteProcess(
            cmd=[
                'ros2', 'topic', 'pub', '/calibrated', 'std_msgs/Bool', '{data: true}'
            ],
            name='fake_joint_calibration'
        )
    ])

