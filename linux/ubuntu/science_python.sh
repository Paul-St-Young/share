#!/bin/bash
sudo apt-get update

sudo apt-get install python-pip -y

sudo -H pip install --upgrade pip
sudo -H pip install jupyter numpy scipy pandas

sudo apt-get install libfreetype6-dev -y
sudo -H pip install matplotlib
