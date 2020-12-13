from threading import Thread
import time
import mido

class MidiOut:
    def __init__(self, midiOutSubstring):
        port = [x for x in mido.get_output_names() if midiOutSubstring in x][0]
        self.midiOut = mido.open_output(port)
        #print(mido.get_output_names())
        self.channel = 15

    def sendProgramChange(self, index):
        msg = mido.Message('program_change', channel=self.channel, program =index)
        self.midiOut.send(msg)

    def sendControlChange(self, cntrlId, value):
        #print(f"midi out = {cntrlId} - {value}")
        msg = mido.Message('control_change', channel=self.channel, control=cntrlId, value=value)
        self.midiOut.send(msg)
    
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
                self.processMidi(msg)

    def processMidi(self, msg):
        if msg.channel != 15 and msg.type == "control_change":
            
            #send event
            for handler in self.handlers:
                handler(msg.control, msg.value)

    def OnUpdate(self, handler):
        self.handlers.append(handler)
            
class MidiMaster:
    def __init__(self, midiControlData, midiInSubstring, midiOutSubstring):
        self.__handlers = []
        self.midiOut = MidiOut(midiOutSubstring)
        self.__midiIn = MidiIn(midiInSubstring)
        self.__midiIn.daemon = True #set this thread as a Daemon Thread
        self.__midiIn.OnUpdate(self.midiInHandler)
        self.__midiIn.start()

        self.__midiControlData = midiControlData

    def onUpdate(self, handler):
        self.__handlers.append(handler)

    def sendControlOutputForControlName(self,controlName, value):
        controlId = int(self.__midiControlData[controlName]["midi_out_control"])
        midiVal = int(value)/100 * 127
        self.midiOut.sendControlChange(int(controlId), int(midiVal))

    def midiInHandler(self, controlId, value):
        #if controlId is in midiControlData send out event
        for key, dictVal in self.__midiControlData.items():
            
            id = dictVal.get('midi_in_control', None)
            if id is not None and int(id) == controlId:
                controlName = key
                #send midi out to synth
                outId = dictVal.get('midi_out_control', None)
                self.midiOut.sendControlChange(int(outId), int(value))
                scaledVal = int(value)/127 * 100
                #produce Event
                #print (f"Send midi in event: {key}-{scaledVal}")
                for handler in self.__handlers:
                    handler(controlName, scaledVal)
                break
