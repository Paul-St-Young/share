#!/bin/bash

# make sure everything is up to date (Software Updator)
sudo apt-get update
sudo apt-get upgrade

# scripting essentials
# ------------------------------
sudo apt-get install vim git
sudo apt-get install python-dev
#sudo apt-get install python-pip # this is lazy and bad but it works
sudo pip install jupyter
# InsecurePlatformWarning: either upgrade to python 2.7.9 or use pyOpenSSL
sudo apt-get install gfortran
sudo apt-get install liblapack-dev
sudo pip install scipy

sudo add-apt-repository ppa:staticfloat/juliareleases
sudo add-apt-repository ppa:staticfloat/julia-deps
sudo apt-get update
sudo apt-get install julia

echo "Pkg.update()" | julia 
echo "Pkg.add(\"IJulia\")" | julia # ? does not match cache
echo "Pkg.build()" | julia
# at this point julia should work in jupyter

echo "Pkg.add(\"PyPlot\")" | julia
