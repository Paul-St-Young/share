#!/bin/bash

VERSION=3.2.10

# 1. acquire the latest module (Google "module download")
wget http://sourceforge.net/projects/modules/files/Modules/modules-$VERSION/modules-$VERSION.tar.gz
tar -zxvf modules-$VERSION.tar.gz
cd modules-$VERSION

# 2. install tcl header & library, on Ubuntu 14.04: 
sudo apt-get install tcl8.6-dev -y

# 3. configure while enabling a deprecated feature
CPPFLAGS="-DUSE_INTERP_ERRORLINE" ./configure

# 4. make & install
make; sudo make install

# 5. make a symbolic link to the current version
cd /usr/local/Modules
sudo ln -s $VERSION default

# 6. make an init script publicly available (sh is most compatible)
sudo cp /usr/local/Modules/default/init/bash /etc/profile.d/modules.sh
sudo chmod 755 /etc/profile.d/modules.sh

# 7. execute modules.sh on startup
# append ". /etc/profile.d/modules.sh" to ~/.bashrc
