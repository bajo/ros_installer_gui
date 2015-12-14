# ros_installer_gui
Simple python (tkinter) based gui for ROS install process

The installer process for [ROS](http://www.ros.org) in a simple gui.

Dependency: python 2, and tkinter
sudo apt-get install python-tk

Simply run ``` python tkmain.py``` as a user who is able to run sudo commands.
Do not run as root or directly with ```sudo``` as it will otherwise write the wrong shell configuration files and it is not recommended to run ```rosdep update``` as root.

Users are able to choose different settings for:
- mirror from which ROS will be installed
- ros version (indigo or jade)
- default packages (desktop, desktop-full or ros-base)
- default shell (bash or zsh)
- install [catkin tools](https://catkin-tools.readthedocs.org) 

After this tool is finished the user should only need to create a catkin workspace.
