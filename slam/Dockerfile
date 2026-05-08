# This is a custom-made image for simulating the new version of VRX
# With ROS2, Ubuntu 24.04 and new Gazebo
FROM osrf/ros:jazzy-desktop-full

SHELL ["/bin/bash", "-c"] 

# Install IGN Gazebo Harmonic
RUN apt-get update && sudo apt-get install lsb-release wget gnupg nano inetutils-ping -y
RUN apt install git build-essential cmake genromfs python3-pip python3-venv -y

RUN lsb_release -cs
RUN dpkg --print-architecture
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
RUN apt-get update && apt-cache search gz- && apt-get install gz-harmonic -y

RUN apt install ros-jazzy-ros-gz-interfaces ros-jazzy-xacro ros-jazzy-joy-teleop ros-jazzy-gps-msgs -y

RUN apt install ros-jazzy-joy ros-jazzy-teleop-twist-joy \
    ros-jazzy-teleop-twist-keyboard ros-jazzy-laser-proc \
    ros-jazzy-nav2-amcl ros-jazzy-nav2-map-server \
    ros-jazzy-moveit ros-jazzy-urdf ros-jazzy-xacro \
    ros-jazzy-compressed-image-transport ros-jazzy-rqt* ros-jazzy-rviz2 \
    ros-jazzy-cartographer ros-jazzy-navigation2 ros-jazzy-interactive-markers \
    ros-jazzy-vision-msgs ros-jazzy-urg-node ros-jazzy-rplidar-ros -y

# ROS packages for Turtlebot3 robot     
RUN sudo apt install -y ros-jazzy-dynamixel-sdk \
    ros-jazzy-turtlebot3-*

# We also install Git and other tools
RUN sudo apt install -y git vim nano iputils-ping net-tools

# MESA drivers for hardware acceleration graphics (Gazebo and RViz)
RUN sudo apt -y install libgl1 libgl1-mesa-dri

# Multiple terminals support (tmux)
RUN apt install -y tmuxinator

RUN apt install libspdlog-dev libceres-dev -y    


# By default the DockerFile uses the root as user. 
# We will add a custom user so that we work in user space by default
# And then switch to that user
# Source: https://www.docker.com/blog/understanding-the-docker-user-instruction/
RUN useradd -ms /bin/bash rssa
# Sometimes it is good to add a password so that we can use sudo to install things
# To this end, uncomment the following line, remove extra ### and change the password 
RUN echo "rssa:rssa" | chpasswd 
### Remove #### to change the password
RUN adduser rssa sudo & adduser rssa dialout & adduser rssa plugdev
RUN usermod -aG dialout rssa  && usermod -aG plugdev rssa  && usermod -aG sudo rssa 

# For the real robots. Please see how to share USB from windows via usbipd 
RUN apt -y install usbutils udev

RUN apt install -y ros-jazzy-turtlebot3-msgs ros-jazzy-turtlebot3 \
    ros-jazzy-turtlebot3-simulations ros-jazzy-turtlebot3-navigation2 ros-jazzy-turtlebot3-teleop 
    
# Test the GUI

RUN apt update && apt install -y x11-apps mesa-utils

USER rssa

# We will use the home directory as work directory
# So that the docker starts at HOME!
WORKDIR "/home/rssa"
ENV HOME="/home/rssa"

