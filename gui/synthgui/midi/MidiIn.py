from threading import Thread
import mido

class MidiIn(Thread):
    def __init__(self):
        Thread.__init__(self)
        print(mido.get_input_names())
        self.handlers = []
        print("midi in")
        print(mido.get_input_names())
        self.__midiInList = [mido.open_input(x) for x in mido.get_input_names()]       

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            for m in self.__midiInList:
                for msg in m:
                    #print(msg)
                    self.processMidi(msg)

    def processMidi(self, msg):
        if msg.channel != 15 and msg.type == "control_change":
            
            #send event
            for handler in self.handlers:
                handler(msg.control, msg.value)

    def OnUpdate(self, handler):
        self.handlers.append(handler)