#!/usr/bin/python

__author__ = 'Markus Bajones'
__license__ = 'GPL'
__version__ = '1.0.0'
__email__ = 'markus.bajones@gmail.com'

"""
- download ROS key from keyserver and install it
- show settings (mirror/package selection/ROS distro)
- install selected packages
- rosdep update, and init
"""

import ImageTk
import Tkinter as tk
import ttk as ttk
import subprocess
import os

class ROSInstallerGUI:
    def __init__(self, master):
        self.packages = [('Full desktop install (recommended)', 'desktop-full'),
                         ('Desktop install', 'desktop'),
                         ('Base install', 'ros-base')]
        self.mirrors = [
            ('packages.ros.org', 'http://packages.ros.org'),
            ('mirrors.ustc.edu.cn', 'http://mirrors.ustc.edu.cn'),
            ('mirror.sysu.edu.cn', 'http://mirror.sysu.edu.cn'),
            ('ros.exbot.net', 'http://ros.exbot.net'),
            ('mirror-eu.packages.ros.org', 'http://mirror-eu.packages.ros.org'),
            ('mirror-ap.packages.ros.org', 'http://mirror-ap.packages.ros.org'),
            ('packages.ros.org.ros.informatik.uni-freiburg.de', 'http://packages.ros.org.ros.informatik.uni-freiburg.de'),
            ('mirror.umd.edu/packages.ros.org', 'http://mirror.umd.edu/packages.ros.org'),
            ('mobilerobots.case.edu/mirror/packages.ros.org', 'http://mobilerobots.case.edu/mirror/packages.ros.org'),
            ('ros.fei.edu.br/archive-ros/packages.ros.org', 'http://ros.fei.edu.br/archive-ros/packages.ros.org'),
            ('ftp.tudelft.nl', 'http://ftp.tudelft.nl')
        ]
        self.ros_version = ['indigo', 'jade']
        self.shell = ['bash', 'zsh']

        self.select_pkg = tk.StringVar()
        self.select_mirror = tk.StringVar()
        self.select_ros_version = tk.StringVar()
        self.select_shell = tk.StringVar()

        self.select_catkin = tk.IntVar()

        self.select_pkg.set('desktop-full')
        self.select_mirror.set('http://packages.ros.org')
        self.select_ros_version.set('indigo')
        self.select_shell.set('bash')
        self.select_catkin.set(1)

        self.installed, self.rosdep_update, self.shell_written = False, False, False

        self.master = master
        master.title("ROS Installer GUI")

        photoimage = ImageTk.PhotoImage(file="rosorg-logo1.png")
        label = tk.Label(image=photoimage)
        label.image = photoimage
        label.pack(fill=tk.X)

        self.settings_button = tk.Button(master, text="Customize settings", command=self.show_settings)
        self.settings_button.pack(fill=tk.X)

        self.message = tk.StringVar()
        self.message.set('Install ROS and initalize rosdep')
        self.install_button = tk.Button(master, textvariable=self.message, command=self.install_ros)
        self.install_button.pack(fill=tk.X)

        self.shell_button = tk.Button(master, text='Setup shell configuration', command=self.write_shell_config)
        self.shell_button.pack(fill=tk.X)

        self.close_button = tk.Button(master, text="Close", command=self.explain_next_steps)
        self.close_button.pack(fill=tk.X)


    def show_settings(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("Settings")

        self.notebook = ttk.Notebook(self.newWindow)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='ROS version and packages')
        self.notebook.add(self.tab2, text='ROS version')
        self.notebook.add(self.tab3, text='Shell')
        self.notebook.add(self.tab4, text='Mirrors')
        self.notebook.pack(fill=tk.X)

        for text, pkg in self.packages:
            b = tk.Radiobutton(self.tab1, text=text, variable=self.select_pkg, value=pkg)
            b.pack(anchor=tk.W)
        b = tk.Checkbutton(self.tab1, text="Include catkin tools?", variable=self.select_catkin)
        b.pack(anchor=tk.W)

        for text in self.ros_version:
            b = tk.Radiobutton(self.tab2, text=text, variable=self.select_ros_version, value=text)
            b.pack(anchor=tk.W)

        for text in self.shell:
            b = tk.Radiobutton(self.tab3, text=text, variable=self.select_shell, value=text)
            b.pack(anchor=tk.W)

        for text, mirror in self.mirrors:
            b = tk.Radiobutton(self.tab4, text=text, variable=self.select_mirror, value=mirror)
            b.pack(anchor=tk.W)

        button = tk.Button(self.newWindow, text ="Done", command = self.newWindow.destroy)
        button.pack()

    def explain_next_steps(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Final steps')

        message = tk.StringVar()
        if self.installed and self.rosdep_update and self.shell_written:
            message.set('ROS installed, rosdep updated and .{}rc written.\n'
                        'Next you need to create a catkin workspace'.format(self.select_shell.get()))
        else:
            message.set('Some step did not execute or had an error.\n\n'
                        'If you think this is fine you can proceed to create your catkin workspace.\n'
                        'Otherwise check the output on the terminal for more information.')
        label = tk.Label(self.newWindow, textvariable=message, anchor=tk.W, justify=tk.LEFT)
        label.pack()
        button = tk.Button(self.newWindow, text ="Done", command = self.master.quit)
        button.pack()


    def install_ros(self):
        self.message.set('Executing...')
        self.install_button.config(bg='green')
        self.master.update()
        mirror, ros_pkgs, ros_version = self.select_mirror.get(), self.select_pkg.get(), self.select_ros_version.get()
        ros_pkgs = '-'.join(['ros', ros_version, ros_pkgs])
        catkin =''
        if self.select_catkin.get():
            catkin = 'python-catkin-tools'
        print(mirror, ros_version, ros_pkgs, catkin)

        try:
            subprocess.call(['gksudo', 'python root_tools.py', mirror, ros_version, ros_pkgs, catkin])
            self.message.set('Done')
            self.update_rosdep()
            self.installed = True
        except CalledProcessError as e:
            self.message.set('Something went wrong. Please check the terminal output')
            self.install_button.config(bg='red')
            self.installed = False
        self.master.update()

    def update_rosdep(self):
        try:
            subprocess.check_call(['/usr/bin/rosdep', 'update'])

        except CalledProcessError as e:
            print("rosdep executed with errors. [{err}]".format(err=str(e)))
            self.rosdep_update = False

    def write_shell_config(self):
        shell = self.select_shell.get()
        print(shell)
        content = "".join(['source /opt/ros/', self.select_ros_version.get(), '/setup.', shell])
        file = os.path.join(os.environ['HOME'], "".join(['.',shell,'rc']))
        try:
            if not os.path.exists(file) or not content in open(file).read():
                with open(file, 'a+') as f:
                    #f.write(content+'\n')
                    print("{file} written successfully.".format(file=file))
            else:
                print("'{}' already in {}".format(content, file))
            self.shell_written = True
        except IOError as e:
            print('Could not read or write {file}. Error was {err}'.format(file=file, err=e))
            self.shell_written = False
        self.shell_button.config(bg='green')
        self.master.update()


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = ROSInstallerGUI(root)
    root.mainloop()