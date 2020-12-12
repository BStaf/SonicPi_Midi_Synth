from tkinter import * 
from MidiHelpers import *
from AppPalette import *
from MainPage import *
from InstSettingsPage import *
from InstrumentPage import *

import tkinter.font as tkFont
import os
import json
import copy

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
        self.__curInstSettings = {}
        self.__loadCurrentSettings()

    def getInstrumentList(self):
        return list(self.instrumentData.keys())

    def getCurentSettings(self):
        return self.__curInstSettings.items()

    def setInstrument(self, instrumentName):
        self.currentInstrument = instrumentName
        index = self.getInstrumentList().index(self.currentInstrument)
        self.__midiMaster.midiOut.sendProgramChange(index)
        self.__loadCurrentSettings()

    def setInstrumentSetting(self, settingName, value):
      #  val = value / 100.0
        self.__curInstSettings[settingName] = float(value)/100
        self.__midiMaster.sendControlOutputForControlName(settingName, value)
        
    def __loadCurrentSettings(self):
        self.__curInstSettings = copy.deepcopy(self.instrumentData[self.currentInstrument])
        i = 0
        for key, value in self.__curInstSettings.items():
            if i > 4:
                break
            print(f"set {key} - {value}")
            self.setInstrumentSetting(key,float(value)*100)
            i = i+1



class MainFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        pages = {}

        pages["instConfigPage"] = InstSettingsPage(pages, instruments, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["mainPage"] = MainPage(pages, instruments, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["instSelectPage"] = InstrumentPage(pages, instruments, root, width=windowWidth, height=windowHeight)

        container = Frame(self)
        container.pack(fill="both", expand=True)

        for key, value in pages.items():
             value.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        pages["mainPage"].show()
   
with open(instrumentJsonPath, 'r') as reader:
    instrumentData = json.load(reader)

with open(midiControlJsonPath, 'r') as reader:
    midiControlData = json.load(reader)

midiMaster = MidiMaster(midiControlData, midiInSubstring, midiOutSubstring)
instruments = Instruments(instrumentData, "piano", midiMaster)

root = Tk() 
root.wm_attributes('-type', 'splash')
root.geometry(f"{windowWidth}x{windowHeight}")

main = MainFrame(root)
main.pack(side="top", fill="both", expand=True)

mainloop() 
