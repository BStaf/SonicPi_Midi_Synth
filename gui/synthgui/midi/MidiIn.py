from threading import Thread
import mido

class MidiIn(Thread):
    def __init__(self, midiInSubstring):
        Thread.__init__(self)
        print(mido.get_input_names())
        self.handlers = []
        port = [x for x in mido.get_input_names() if midiInSubstring in x][0] 
        self.midiIn = mido.open_input(port)

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            for msg in self.midiIn:
                #print(msg)
                self.processMidi(msg)

    def processMidi(self, msg):
        if msg.channel != 15 and msg.type == "control_change":
            
            #send event
            for handler in self.handlers:
                handler(msg.control, msg.value)

    def OnUpdate(self, handler):
        self.handlers.append(handler)