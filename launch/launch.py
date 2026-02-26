from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare the argument to allow recognition
    use_gst_timestamps_arg = DeclareLaunchArgument(
        'use_gst_timestamps',
        default_value='False',
        description='Use gst time instead of ROS time'
    )

    use_gst_timestamps_val = LaunchConfiguration('use_gst_timestamps')

     # Define the GStreamer pipelines for both the M0161 camera and Boson thermal camera. Make sure to add your IP addressa and port number
    normal_cam_config = "rtspsrc location=rtsp://<<ip address of the drone>>:<<port number>>/live protocols=tcp latency=0 ! decodebin ! videoconvert"
    thermal_cam_config = "rtspsrc location=rtsp://<<ip address of the drone>>:<<port number>>/live protocols=tcp latency=0 ! decodebin ! videoconvert"

    return LaunchDescription([
        use_gst_timestamps_arg, 
        
        Node(
            package='gscam2',
            executable='gscam_main',
            name='gscam_normal',
            parameters=[
                {'gscam_config': normal_cam_config},
                {'use_gst_timestamps': use_gst_timestamps_val},
            ],
            remappings=[('/image_raw', '/camera/image_raw')]
        ),
        Node(
            package='gscam2',
            executable='gscam_main',
            name='gscam_thermal',
            parameters=[
                {'gscam_config': thermal_cam_config},
                {'use_gst_timestamps': use_gst_timestamps_val},
            ],
            remappings=[('/image_raw', '/thermal/image_raw')]
        )
    ])