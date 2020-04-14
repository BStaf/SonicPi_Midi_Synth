#!/bin/sh
wget -nc http://r.newman.ch/rpi/sonic-pi-3.2.2/sonic-pi-3.2.2_1.armhf.deb
sudo rpi-update
sudo apt install -y ruby
sudo apt install -y ./sonic-pi-3.2.2_1.armhf.deb

