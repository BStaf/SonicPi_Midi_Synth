jackd -d alsa --device hw:0 --rate 44100 --period 1024 &
sleep 3
sonic-pi-tool.py start-server --path /opt/sonic-pi-3.2.2/ &
sleep 23
sonic-pi-tool.py run-file midiSynth.rb



