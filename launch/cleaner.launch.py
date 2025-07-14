# Copyright 2024 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.actions import AppendEnvironmentVariable
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    # Launch Arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    # robot_name = LaunchConfiguration('robot_name', default='limo')
    # world = LaunchConfiguration('world', default='empty.sdf')

    # # Pose where we want to spawn the robot
    # spawn_x_val = '9.073496746393584'
    # spawn_y_val = '0'
    # spawn_z_val = '0.'
    # spawn_yaw_val = '1.57'
    
    rviz_config_file = PathJoinSubstitution(
        [
            FindPackageShare('cleaner_description'),
            'rviz',
            'cleaner_visual.rviz',
        ]
    )

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            ' ',
            PathJoinSubstitution(
                [FindPackageShare('cleaner_description'),
                'urdf', 'cleaner.xacro']
            ),
        ]
    )
    robot_description = {'robot_description': robot_description_content}
    # Launch RViz
    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )

    # Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': use_sim_time}]
    )
    
    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )
    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher_gui,
        start_rviz_cmd

    ])