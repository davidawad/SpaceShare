#!/bin/bash
echo "Running System Renovations ..."


sudo apt-get install -y && sudo apt-get upgrade -y && sudo apt-get autoremove -y

sudo apt-get dist-upgrade

sudo apt-get -f install && sudo apt-get -y autoclean && sudo apt-get -y clean


echo "System Renovations Complete" 
echo "Please Come Again"


