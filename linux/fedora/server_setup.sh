#!/bin/bash

# module command will be enabled the next time shell sources /etc/share/Modules/init/[shell]
sudo dnf install environment-modules.x86_64 -y

# Red Hat equilalent of 'build-essentials'
sudo dnf groupinstall "Development Tools" -y # include Boost
sudo dnf groupinstall "Development Libraries" -y

# C++ development
sudo dnf install gcc-c++.x86_64 cmake.x86_64 -y

# QMCPACK dependencies
sudo dnf install libxml2-devel.x86_64 hdf5-devel.x86_64 boost-devel.x86_64 -y
