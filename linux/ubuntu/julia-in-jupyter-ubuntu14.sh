#!/bin/bash

# make sure everything is up to date (Software Updator)
sudo apt-get update

# scripting essentials
# ------------------------------
# dependencies
#sudo apt-get install python-dev
#sudo apt-get install python-pip
#sudo pip -H install jupyter
# InsecurePlatformWarning: either upgrade to python 2.7.9 or use pyOpenSSL
#sudo apt-get install gfortran
#sudo apt-get install liblapack-dev
#sudo pip install scipy

# install julia
sudo add-apt-repository ppa:staticfloat/juliareleases -y
sudo add-apt-repository ppa:staticfloat/julia-deps -y
sudo apt-get update
sudo apt-get install julia -y

# setup in jupyter
echo "Pkg.update()" | julia 
echo "Pkg.add(\"IJulia\")" | julia # ? does not match cache
echo "Pkg.build()" | julia
# at this point julia should work in jupyter
