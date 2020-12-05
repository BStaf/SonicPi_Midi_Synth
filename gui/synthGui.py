from tkinter import * 
from AppPalette import *
from MainPage import *

import tkinter.font as tkFont
import mido
import os

guiPicName = os.path.dirname(os.path.realpath(__file__)) + "/guiMain.png"

instrumentList = [
    "piano", 
    "prophet", 
    "blade",
    "tb303",
    "mod_fm",
    "hoover",
    "zawa",
    "pluck",
    "dull_bell",
    "pretty_bell",
    "beep",
    "sine",
    "saw",
    "pulse",
    "subpulse"
    ]

class MidiOut:
    def __init__(self):
        #port = [x for x in mido.get_output_names() if "Midi Through" in x][0]
        #self.midiOut = mido.open_output(port)
        self.midiOut = mido.open_output(mido.get_output_names()[1])

    def sendProgramChange(self, index):
        msg = mido.Message('program_change', program =index)
        self.midiOut.send(msg)

    def sendControlChange(self, cntrlId, value):
        msg = mido.Message('control_change', channel=1, control=cntrlId, value=value)
        self.midiOut.send(msg)

midiOut = MidiOut()

root = Tk()      
#root.wm_attributes('-type', 'splash')
windowHeight = 320
windowWidth = 480
root.geometry(f"{windowWidth}x{windowHeight}")

#bigfont = tkFont.Font(family="Helvetica",size=17)
#root.option_add("*Font", bigfont)

main = MainPage(instrumentList, midiOut, root, width=windowWidth, height=windowHeight)
main.pack(fill="both", expand=True)

mainloop() 

