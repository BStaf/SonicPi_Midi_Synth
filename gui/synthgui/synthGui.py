from tkinter import * 
import tkinter.font as tkFont
import os
import json

from AppPalette import *
from pages.FxSettingsPage import *
from pages.FxPage import *
from pages.MainPage import *
from pages.InstSettingsPage import *
from pages.InstrumentPage import *
from pages.SynthObjectSettingsPage import *
from midi.MidiHelpers import *
from synth_objects.Fxs import *
from synth_objects.Instruments import *


instrumentJsonPath = os.path.dirname(os.path.realpath(__file__)) + "/config/InstrumentData.Json"
instrumentParamsPath = os.path.dirname(os.path.realpath(__file__)) +"/config/InstrumentParameters.Json"
fxJsonPath = os.path.dirname(os.path.realpath(__file__)) + "/config/FxData.Json"
fxParamsPath = os.path.dirname(os.path.realpath(__file__)) +"/config/FxParameters.Json"
midiControlJsonPath = os.path.dirname(os.path.realpath(__file__)) + "/config/ControlData.Json"

#midiInSubstring = "Arduino"
midiInSubstring = "VMPK"#"loop"
#midiOutSubstring = "Midi Through"
midiOutSubstring = "RtMidi"#"loop"

windowHeight = 320
windowWidth = 480

class MainFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        pages = {}

        pages["instConfigPage"] = SynthObjectSettingsPage(pages, instruments, "mainPage", root, width=windowWidth, height=windowHeight)
        #pages["instConfigPage"] = InstSettingsPage(pages, instruments, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["mainPage"] = MainPage(pages, instruments, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["instSelectPage"] = InstrumentPage(pages, instruments, root, width=windowWidth, height=windowHeight)
        pages["fxConfigPage"] = FxSettingsPage(pages, fxs, "fxSelectPage", root, width=windowWidth, height=windowHeight)
        #pages["fxConfigPage"] = InstSettingsPage(pages, fxs, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["fxSelectPage"] = FxPage(pages, fxs, root, width=windowWidth, height=windowHeight)
        

        container = Frame(self)
        container.pack(fill="both", expand=True)

        for key, value in pages.items():
             value.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        pages["mainPage"].show()
   
with open(instrumentJsonPath, 'r') as reader:
    instrumentData = json.load(reader)

with open(midiControlJsonPath, 'r') as reader:
    midiControlData = json.load(reader)

with open(instrumentParamsPath, 'r') as reader:
    instrumentParamsData = json.load(reader)

with open(fxJsonPath, 'r') as reader:
    fxData = json.load(reader)

with open(fxParamsPath, 'r') as reader:
    fxParamsData = json.load(reader)

midiMaster = MidiMaster(midiControlData, midiInSubstring, midiOutSubstring)
instruments = Instruments(instrumentData, instrumentParamsData, "piano", midiMaster)
fxs = Fxs(fxData, fxParamsData, midiMaster)

root = Tk() 
root.wm_attributes('-type', 'splash')
root.geometry(f"{windowWidth}x{windowHeight}")

main = MainFrame(root)
main.pack(side="top", fill="both", expand=True)

mainloop() 
