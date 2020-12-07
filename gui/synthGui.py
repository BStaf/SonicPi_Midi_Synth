from threading import Thread
import time

from tkinter import * 
from AppPalette import *
from MainPage import *
from NextPage import *

import tkinter.font as tkFont
import mido
import os
import json

instrumentJsonPath = os.path.dirname(os.path.realpath(__file__)) + "/InstrumentData.Json"

windowHeight = 320
windowWidth = 480

# instrumentList = [
#     "piano", 
#     "prophet", 
#     "blade",
#     "tb303",
#     "mod_fm",
#     "hoover",
#     "zawa",
#     "pluck",
#     "dull_bell",
#     "pretty_bell",
#     "beep",
#     "sine",
#     "saw",
#     "pulse",
#     "subpulse"
#     ]

def loadInstrumentData(josnFilePath):
    return json.load(josnFilePath)

class MidiOut:
    def __init__(self):
        #port = [x for x in mido.get_output_names() if "Midi Through" in x][0]
        #self.midiOut = mido.open_output(port)
        self.channel = 15
        self.midiOut = mido.open_output(mido.get_output_names()[1])

    def sendProgramChange(self, index):
        msg = mido.Message('program_change', channel=self.channel, program =index)
        self.midiOut.send(msg)

    def sendControlChange(self, cntrlId, value):
        msg = mido.Message('control_change', channel=self.channel, control=cntrlId, value=value)
        self.midiOut.send(msg)

class MidiIn(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.handlers = []
        self.midiIn = mido.open_input(mido.get_input_names()[0])

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

def midiInHandler(control, value):
    print(f"{control}-{value}")
    
instrumentData = loadInstrumentData(instrumentJsonPath)

midiOut = MidiOut()
midiIn = MidiIn()
midiIn.daemon = True #set this thread as a Daemon Thread
#midiIn.OnUpdate(midiInHandler)

root = Tk() 
root.geometry(f"{windowWidth}x{windowHeight}")

#main = MainPage(instrumentList, midiOut, root, width=windowWidth, height=windowHeight)
main = NextPage(instrumentData.keys(), midiOut, midiIn, root, width=windowWidth, height=windowHeight)

main.pack(fill="both", expand=True)

midiIn.start()
mainloop() 
