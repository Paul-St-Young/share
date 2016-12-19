#!/bin/bash

# module command will be enabled the next time shell sources /etc/share/Modules/init/[shell]
sudo dnf install environment-modules.x86_64 -y

# Red Hat equilalent of 'build-essentials'
sudo dnf groupinstall "Development Tools" -y
sudo dnf groupinstall "Development Libraries" -y

# ?requirement for Intel compilers
#sudo dnf install kernel-devel -y
#sudo dnf install gtk3.x86_64 -y
