#!/bin/bash
# source: VIM and Python - a Match Made in Heaven, Real Python
#  https://realpython.com/blog/python/vim-and-python-a-match-made-in-heaven

sudo dnf install python-devel -y # "Python.h"
sudo dnf install python3-tkinter.x86_64 -y
# tkinter is needed by matplotlib.pyplot
## if GPU supports OpenGL, then use QT5 rather than TkAgg backend
#sudo dnf install PyQt5 -y
#echo "backend : Qt5Agg" > ~/.config/matplotlib/matplotlibrc

## solve 'gcc error:/usr/lib/rpm/redhat/redhat-hardened-cc1: No such file or directory'
#sudo dnf install redhat-rpm-config -y

#pip install --upgrade pip  # bad idea to upgrade pip beyond system support
pip install --user numpy scipy pandas matplotlib
pip install --user lxml h5py #scikit-image
