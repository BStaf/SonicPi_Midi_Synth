from tkinter import * 
from MidiHelpers import *
from AppPalette import *
from MainPage import *
from NextPage import *
from InstrumentPage import *

import tkinter.font as tkFont
import os
import json

instrumentJsonPath = os.path.dirname(os.path.realpath(__file__)) + "/InstrumentData.Json"
midiControlJsonPath = os.path.dirname(os.path.realpath(__file__)) + "/ControlData.Json"

midiInSubstring = "Arduino"
#midiInSubstring = "loop"
midiOutSubstring = "Midi Through"
#midiOutSubstring = "loop"

windowHeight = 320
windowWidth = 480

class Instruments:
    def __init__(self, instrumentData, firstInstrument, midiMaster):
        self.instrumentData = instrumentData
        self.currentInstrument = firstInstrument
        self.__midiMaster = midiMaster

    def getInstrumentList(self):
        return list(self.instrumentData.keys())

    def getInstrumentData(self):
        return self.instrumentData[self.currentInstrument].items()

    def setInstrument(self, instrumentName):
        self.currentInstrument = instrumentName
        index = self.getInstrumentList().index(self.currentInstrument)
        self.__midiMaster.midiOut.sendProgramChange(index)

class MainFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        pages = {}

        pages["instConfigPage"] = NextPage(pages, instruments, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["mainPage"] = MainPage(pages, instruments, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["instSelectPage"] = InstrumentPage(pages, instruments, root, width=windowWidth, height=windowHeight)

        container = Frame(self)
        container.pack(fill="both", expand=True)

        for key, value in pages.items():
             value.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        pages["instSelectPage"].show()
   
with open(instrumentJsonPath, 'r') as reader:
    instrumentData = json.load(reader)

with open(midiControlJsonPath, 'r') as reader:
    midiControlData = json.load(reader)

midiMaster = MidiMaster(midiControlData, midiInSubstring, midiOutSubstring)
instruments = Instruments(instrumentData, "piano", midiMaster)

root = Tk() 
root.wm_attributes('-type', 'splash')
root.geometry(f"{windowWidth}x{windowHeight}")
#bigfont = tkFont.Font(family="Helvetica",size=17)
#root.option_add("*Font", bigfont)


main = MainFrame(root)
main.pack(side="top", fill="both", expand=True)

mainloop() 
