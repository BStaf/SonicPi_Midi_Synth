import mido

class MidiOut:
    def __init__(self, midiOutSubstring):
        port = [x for x in mido.get_output_names()][0]
       # port = [x for x in mido.get_output_names() if midiOutSubstring in x][0]
        self.midiOut = mido.open_output(port)
        print("midi out")
        print(mido.get_output_names())
        self.channel = 15

    def sendProgramChange(self, index):
        msg = mido.Message('program_change', channel=self.channel, program =index)
        self.midiOut.send(msg)

    def sendControlChange(self, cntrlId, value):
        #print(f"midi out = {cntrlId} - {value}")
        msg = mido.Message('control_change', channel=self.channel, control=cntrlId, value=value)
        self.midiOut.send(msg)