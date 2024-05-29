import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, EmitEvent, UnregisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.events.lifecycle import ChangeState
from launch.event_handlers import OnProcessExit
from lifecycle_msgs.msg import Transition

def generate_launch_description():
    pkg_share = get_package_share_directory('autonomous_exploration')
    world_file = os.path.join(pkg_share, 'worlds', 'finally')

    # Запускаем Gazebo с указанным миром
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', world_file],
        output='screen'
    )

    # Публикуем статические трансформации
    laser_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'base_footprint', 'laser_frame']
    )

    odom_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_footprint']
    )

    # Запускаем SLAM Toolbox
    slam_toolbox_file = os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_toolbox_file)
    )

    # Создаем узел для navigation2
    nav2_pkg_prefix = get_package_share_directory('turtlebot3_navigation2')
    nav2_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_pkg_prefix, 'launch', 'navigation2.launch.py')),
        launch_arguments={'map': 'my_map.yaml'}.items()
    )

    # Запускаем пакет
    control_node = Node(
        package='autonomous_exploration',
        executable='control',
        name='control_node',
        output='screen'
    )

    # Создаем LaunchDescription с указанными действиями
    return LaunchDescription([
        gazebo,
        laser_tf,
        odom_tf,
        slam_toolbox,
        control_node,
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=control_node,
                on_exit=[
                    EmitEvent(event=ChangeState(
                        lifecycle_node_matcher='slam_toolbox',
                        transition_id=Transition.TRANSITION_ACTIVE_SHUTDOWN
                    )),
                    EmitEvent(event=ChangeState(
                        lifecycle_node_matcher='Exploration',
                        transition_id=Transition.TRANSITION_ACTIVE_SHUTDOWN
                    )),
                    nav2_node
                ]
            )
        )
    ])