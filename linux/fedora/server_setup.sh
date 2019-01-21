#!/bin/bash

# enable ssh
sudo systemctl enable sshd.service

# Red Hat equilalent of 'build-essentials'
sudo dnf groupinstall "Development Tools" -y # include Boost
sudo dnf groupinstall "Development Libraries" -y

# C++ development
sudo dnf install gcc-c++.x86_64 cmake.x86_64 -y

# QMCPACK dependencies
sudo dnf install libxml2-devel.x86_64 hdf5-devel.x86_64 boost-devel.x86_64 -y
# MPI, LAPACK and FFTW, not necessary if using Intel compilers
sudo dnf install mpich-devel.x86_64 lapack-devel.x86_64 fftw-devel.x86_64 -y
# note: module load mpi to add include and library paths
