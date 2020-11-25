#!/bin/bash
#find usb soundcard.  
soundcard=$(cat /proc/asound/cards | grep -i "USB Audio Device")
soundcard=${soundcard:0:3}
soundcard=${soundcard//[[:blank:]]/}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR

#jackd -d alsa --device hw:3 --rate 44100 --period 256 -n 2 &
jackd -P 70 -d alsa --device hw:$soundcard --rate 44100 --period 256 -n 3 -s &
sleep 3
sonic-pi-tool.py start-server --path /opt/sonic-pi-3.2.2/ > /dev/null 2>&1 &
sleep 40
echo "Run Program"
sonic-pi-tool.py run-file $DIR/midiSynth.rb &> /dev/null 2>&1 &
