import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    
    
    # load urdf
    pkgPth = launch_ros.substitutions.FindPackageShare(package='urdf_test').find('urdf_test')
    urdfModelPath = os.path.join(pkgPth, 'urdf/model2.urdf')

    # load rviz config file
    rviz_config_file = os.path.join(pkgPth,'config/setup.rviz')

    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()

    params = {'robot_description': robot_desc}

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params],
        # arguments=[urdfModelPath]
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[params],
        # arguments=[urdfModelPath],
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

    # gazebo_sever = launch_ros.actions.Node(
    #         package='gazebo_ros',
    #         executable='gzserver',
    #         name='gazebo_server',
    #         # arguments=[world_file],
    #         output='screen'
    # )

    # gazebo_client = launch_ros.actions.Node(
    #         package='gazebo_ros',
    #         executable='gzclient',
    #         name='gazebo_client',
    #         output='screen'
    # )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                             description='this is a flag'),
        launch.actions.DeclareLaunchArgument(name='model',default_value=urdfModelPath,
                                             description='path to the urdf model'),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        # gazebo_sever,
        # gazebo_client,
        rviz_node
     ])