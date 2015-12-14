#!/usr/bin/python
"""
- read output from a subprocess in a background thread
- show the output in the GUI
"""
import Tkinter as tk
import ttk as ttk
import ImageTk

class ROSInstallerGUI:
    def __init__(self, master):
        self.master = master
        master.title("ROS Installer GUI")

        photoimage = ImageTk.PhotoImage(file="rosorg-logo1.png")

        self.label = tk.Label(image=photoimage)
        self.label.image = photoimage
        self.label.pack(fill=tk.X)

        self.install_button = tk.Button(master, text="Install ROS", command=self.greet)
        self.install_button.pack(fill=tk.X)

        self.settings_button = tk.Button(master, text="Show Settings", command=self.show_settings)
        self.settings_button.pack(fill=tk.X)

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack(fill=tk.X)

    def show_settings(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ROSSettings(self.newWindow)

    def greet(self):
        print('greetings')

class ROSSettings():
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

        self.master = master

        self.select_pkg = tk.StringVar()
        self.select_pkg.set('desktop-full')
        self.select_mirror = tk.StringVar()
        self.select_mirror.set('http://packages.ros.org')

        self.notebook = ttk.Notebook(self.master)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Packages')
        self.notebook.add(self.tab2, text='Mirrors')
        self.notebook.pack(fill=tk.X)

        for text, pkg in self.packages:
            b = tk.Radiobutton(self.tab1, text=text, variable=self.select_pkg, value=pkg)
            b.pack(anchor=tk.W)

        for text, mirror in self.mirrors:
            b = tk.Radiobutton(self.tab2, text=text, variable=self.select_mirror, value=mirror)
            b.pack(anchor=tk.W)

        self.quitButton = tk.Button(self.master, text = 'Done', width = 25, command = self.close_window)
        self.quitButton.pack()
    def close_window(self):
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = ROSInstallerGUI(root)
    root.mainloop()