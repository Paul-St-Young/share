#!/bin/bash

# first steps
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager \
    --add-repo \
    https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf -y install docker-ce

# post installation
sudo groupadd docker
sudo usermod -aG docker $USER
sudo systemctl enable docker

# test
sudo systemctl start docker.service
#docker run hello-world
