#!/bin/bash

# Fedora 23 setup script
# may have to run twice to get everything working

sudo dnf upgrade
sudo dnf group install "C Development Tools and Libraries" 
sudo dnf install redhat-rpm-config # solve redhat-hardened-cc1

sudo dnf install freetype-devel # pre-req. for matplotlib
sudo dnf install python-devel # pre-req. for numpy
sudo dnf install lapack-devel # pre-req. for scipy

sudo pip install --upgrade pip # make sure pip is up to date
sudo pip install jupyter
sudo pip install matplotlib
sudo pip install numpy 
sudo pip install scipy
sudo dnf install julia

# install "IJulia" and "PyPlot" in Julia
echo "Pkg.update()" | julia
echo "Pkg.add(\"IJulia\")" | julia
echo "Pkg.add(\"PyPlot\")" | julia
echo "Pkg.build(\"IJulia\")" | julia # double tap
