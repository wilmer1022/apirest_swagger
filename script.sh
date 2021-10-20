#!/bin/bash

sudo yum install -y vim
sudo yum install -y tree
sudo yum install -y epel-release
sudo yum install -y python3-pip
pip3 --version
sudo pip3 install Flask
pip3 freeze | grep Flask
sudo pip3 install apispec
sudo pip3 install apispec-webframeworks
sudo pip3 install marshmallow
pip3 freeze
#mkdir apirest
#export FLASK_APP=apirest.py
#export FLASK_ENV=development
#flask run --host=0.0.0.0