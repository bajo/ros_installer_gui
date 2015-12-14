#!/usr/bin/python
"""
ROS Installer root utils
Handle the setup and installation of ROS (www.ros,org) in this module.
Needs to run with super user permissions as it needs to make changes in /etc/apt/sources.list.d and installs
packages via apt

Usage:
    root_tools.py <server> <ros_version> <packages>...
    root_tools.py (-h | --help)
    root_tools.py (-v | --version)
Options:
    -h --help       Show this screen.
    -v --version    Show version.
"""

import os
import apt
import sys
import lsb_release
import subprocess
import datetime
from docopt import docopt

__author__ = 'Markus Bajones'
__license__ = 'GPL'
__version__ = '1.0.0'
__email__ = 'markus.bajones@gmail.com'


sources_list = '/etc/apt/sources.list.d/ros-latest.list'
ros_key = '0xB01FA116'
ros_keyserver = 'hkp://pool.sks-keyservers.net:80'

def install_packages(pkgs):
    print("installing {pkgs}".format(pkgs=pkgs))
    cache = apt.cache.Cache()
    cache.update()

    try:
        # prepare all packages for installation
        for i in pkgs:
            pkg = cache[i]
            if pkg.is_installed:
                print("{pkg_name} already installed.".format(pkg_name=i))
            else:
                print("{pkg_name} will be installed.".format(pkg_name=i))
                pkg.mark_install()

            cache.commit()
    except Exception as arg:
        print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))

    return

def write_source_list(server, file):
    if not 'ubuntu' in lsb_release.get_distro_information()['ID'].lower():
        print("Non Ubuntu detected.")
        return False
    codename = lsb_release.get_distro_information()['CODENAME']
    content = 'deb '+server+'/ros/ubuntu '+codename+' main'

    try:
        if not content in open(file).read():
            with open(file, 'w') as f:
                f.write(content)
                print("{file} written successfully.".format(file=file))
        else:
            print("Mirror already in {file}".format(file=file))
    except IOError as e:
        print >> sys.stderr, "Sorry, unable to write file [{err}]".format(err=str(e))
    return True

def add_key_to_system(keyserver, key):
    try:
        subprocess.check_call(["/usr/bin/apt-key", "adv", "--keyserver", keyserver, "--recv-key", key])
    except CalledProcessError as e:
        print >> sys.stderr, "apt-key executed with errors. [{err}]".format(err=str(e))

def check_key_installed(key):
    try:
        proc = subprocess.Popen(["/usr/bin/apt-key", "list"], stdout=subprocess.PIPE)
        while True:
            line = proc.stdout.readline()
            if key.split('0x')[1] in line: # remoce '0x' from the key as it is not shown in apt-key list output
                print('{key} is already installed on this system.'.format(key=key))
                return True
        return False
    except Exception as e:
        print('Error while trying to check for installed GPG key')
        print('Error was: {err}'.format(err=e))
        return False



def init_rosdep():
    if not os.path.exists('/etc/ros/rosdep/sources.list.d/20-default.list'):
        try:
            subprocess.check_call(['/usr/bin/rosdep', 'init'])
        except CalledProcessError as e:
            print >> sys.stderr, "rosdep executed with errors. [{err}]".format(err=str(e))

if __name__ == '__main__':
    arguments = docopt(__doc__, version='ROS Installer root utils 0.1')

    ros_version = arguments['<ros_version>']
    packages = arguments['<packages>']
    server = arguments['<server>']
    print >> sys.stderr, "parameters: [{}, {}, {}]".format(ros_version, server, packages)


    if not os.geteuid() == 0:
        sys.exit('Script must be run as root')
    write_source_list(server, sources_list)
    if not check_key_installed(ros_key):
        add_key_to_system(ros_keyserver, ros_key)
    install_packages(packages)
    init_rosdep()

    exit()