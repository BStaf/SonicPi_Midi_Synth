from .MidiIn import *
from .MidiOut import *

class MidiMaster:
    def __init__(self, midiControlData, midiOutSubstring):
        self.__handlers = []
        self.midiOut = MidiOut(midiOutSubstring)
        self.__midiIn = MidiIn()
        self.__midiIn.daemon = True #set this thread as a Daemon Thread
        self.__midiIn.OnUpdate(self.midiInHandler)
        self.__midiIn.start()

        self.__midiControlData = midiControlData

    def onUpdate(self, handler):
        self.__handlers.append(handler)

    def sendControlOutputForControlName(self, controlName, value):
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
