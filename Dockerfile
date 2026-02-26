ARG TARGET_ROS_DISTRO
ARG IP_ADDRESS

FROM osrf/ros:$TARGET_ROS_DISTRO-desktop

ARG TARGET_ROS_DISTRO
ARG IP_ADDRESS

ENV IP_ADDRESS=$IP_ADDRESS

RUN apt-get update && apt-get upgrade -y

RUN apt-get update \
  && apt-get -y --quiet --no-install-recommends install \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    libgstreamer-plugins-base1.0-dev \
    ros-humble-rmw-cyclonedds-cpp \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /work/my_ws/src

COPY . gscam2

WORKDIR /work/my_ws

RUN apt-get update \
  && rosdep update \
  && rosdep install -y --from-paths . --ignore-src

RUN [ "/bin/bash" , "-c" , "\
  source /opt/ros/$TARGET_ROS_DISTRO/setup.bash \
  && colcon build --event-handlers console_direct+" ]

RUN ["/bin/bash" , "-c" , "echo \"source /opt/ros/$TARGET_ROS_DISTRO/setup.bash\" >> ~/.bashrc"]
RUN ["/bin/bash" , "-c" , "echo \"source /work/my_ws/install/setup.bash\" >> ~/.bashrc"]


CMD ["/bin/bash", "-c", "source install/local_setup.bash \
  && export GSCAM_CONFIG='rtspsrc location=rtsp://$IP_ADDRESS/live protocols=tcp latency=0 ! decodebin ! videoconvert' \
  && ros2 run gscam2 gscam_main"]
