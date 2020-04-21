#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR
#Get latest version
git pull

#jackd -d alsa --device hw:3 --rate 44100 --period 256 -n 2 &
jackd -P 70 -d alsa --device hw:3 --rate 44100 --period 128 -n 3 -s &
sleep 3
sonic-pi-tool.py start-server --path /opt/sonic-pi-3.2.2/ &
sleep 23
sonic-pi-tool.py run-file $DIR/midiSynth.rb
