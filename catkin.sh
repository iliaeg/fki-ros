# No need to #!bin/bash, cuz I want to execute script in current shell

echo "\$ROS_PACKAGE_PATH: "$ROS_PACKAGE_PATH

echo "Setting up catkin for current shell"
source ~/catkin_ws/devel/setup.bash
echo "\$ROS_PACKAGE_PATH: "$ROS_PACKAGE_PATH
