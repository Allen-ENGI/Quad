import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import launch


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'urdf_example'
    file_subpath = 'description/example_robot.urdf.xacro'
    pkg_path = get_package_share_directory(pkg_name)
    rviz_config_file = os.path.join(pkg_path,'worlds/set.rviz')

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    params = {'robot_description': robot_description_raw}

    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params] # add other parameters here if required
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[params],
        arguments=[xacro_file],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d',rviz_config_file],
        output='screen',
        parameters=[params]
    )


    # Run the node
    return LaunchDescription([
                launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                             description='this is a flag'),
        launch.actions.DeclareLaunchArgument(name='model',default_value=xacro_file,
                                             description='path to the urdf model'),
        node_robot_state_publisher,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
