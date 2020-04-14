#!/bin/sh
#Download and install Sonic Pi
wget -nc http://r.newman.ch/rpi/sonic-pi-3.2.2/sonic-pi-3.2.2_1.armhf.deb
sudo rpi-update
sudo apt install -y ruby
sudo apt install -y ./sonic-pi-3.2.2_1.armhf.deb

## Script Uses the sonic-pi-tool python port
## Get whats needed to run script
# Install dependencies:
pip install oscpy click
# Download script:
curl -O https://raw.githubusercontent.com/emlyn/sonic-pi-tool/master/sonic-pi-tool.py
# Make it executable:
chmod +x sonic-pi-tool.py
# Copy it somewhere on the PATH:
sudo cp sonic-pi-tool.py /usr/local/bin/

chmod +x startSynth.sh
#setup to run at startup
CMD=".$PWD/startSynth.sh" 

if grep -q "$CMD" /etc/rc.local; then
  echo "script already set up"
else
  echo "adding startup script to rc.local"
  sed -i '$ d' /etc/rc.local 
  echo "$CMD &" >> /etc/rc.local
  echo "exit 0" >> /etc/rc.local
fi
