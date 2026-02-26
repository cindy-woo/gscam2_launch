from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Define the GStreamer pipelines for both the M0161 camera and Boson thermal camera
    normal_cam_config = "rtspsrc location=rtsp://<<ip address of the drone>>:<<port number>>/live protocols=tcp latency=0 ! decodebin ! videoconvert"
    thermal_cam_config = "rtspsrc location=rtsp://<<ip address of the drone>>:<<port number>>/live protocols=tcp latency=0 ! decodebin ! videoconvert"

    return LaunchDescription([
        # Node 1: M0161 Camera
        Node(
            package='gscam2',
            executable='gscam_main',
            name='gscam_normal',
            parameters=[
                {'gscam_config': normal_cam_config},
            ],
            remappings=[
                ('/image_raw', '/camera/image_raw'),
                ('/camera_info', '/camera/camera_info')
            ]
        ),
        # Node 2: Boson+ FLIR Thermal Camera
        Node(
            package='gscam2',
            executable='gscam_main',
            name='gscam_thermal',
            parameters=[
                {'gscam_config': thermal_cam_config},
            ],
            remappings=[
                ('/image_raw', '/thermal/image_raw'),
                ('/camera_info', '/thermal/camera_info')
            ]
        )
    ])