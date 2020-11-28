import mido
import time
#mido.set_backend('mido.backends.rtmidi_python')
#mido.backend

ports = mido.get_output_names()
print(ports)
midiOut = mido.open_output(ports[2])
#msg = mido.Message('program_change', program =1)
#msg = mido.Message('note_on', note=46, channel=1)

msg = mido.Message('program_change', program=1)
midiOut.send(msg)
time.sleep(10)
# msg = mido.Message('note_on', note=46, channel=1)
# midiOut.send(msg)
# time.sleep(1)
# msg = mido.Message('note_off', note=46, channel=1)
# midiOut.send(msg)
# msg = mido.Message('note_on', note=45, channel=1)
# midiOut.send(msg)
# time.sleep(1)
# msg = mido.Message('note_off', note=45, channel=1)
# midiOut.send(msg)
# msg = mido.Message('note_on', note=44, channel=1)
# midiOut.send(msg)
# time.sleep(1)
# msg = mido.Message('note_off', note=44, channel=1)
# midiOut.send(msg)

midiOut.close()