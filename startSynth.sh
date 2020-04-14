#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

jackd -d alsa --device hw:0 --rate 44100 --period 1024 &
sleep 3
sonic-pi-tool.py start-server --path /opt/sonic-pi-3.2.2/ &
sleep 23
sonic-pi-tool.py run-file $DIR/midiSynth.rb
