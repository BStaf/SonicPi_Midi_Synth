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
instrumentParamsPath = os.path.dirname(os.path.realpath(__file__)) +"/ControlParameters.Json"

midiInSubstring = "Arduino"
#midiInSubstring = "loop"
midiOutSubstring = "Midi Through"
#midiOutSubstring = "loop"

windowHeight = 320
windowWidth = 480

class Instruments:
    def __init__(self, instrumentData, instrumentParamsData, firstInstrument, midiMaster):
        self.__midiUpdateHandlers = []
        self.__instrumentUpdateHandlers = []
        self.currentInstrument = firstInstrument
        self.__instrumentParamsData = instrumentParamsData
        self.instrumentData = self.__filterInstrumentData(instrumentData,instrumentParamsData)
        self.__midiMaster = midiMaster
        self.__midiMaster.onUpdate(self.midiInHandler)
        self.__curInstSettings = {}
        self.__loadCurrentSettings()
        
    def onMidiInUpdate(self, handler):
        self.__midiUpdateHandlers.append(handler)

    def onInstrumentUpdate(self, handler):
        self.__instrumentUpdateHandlers.append(handler)

    def getInstrumentList(self):
        return list(self.instrumentData.keys())

    def getCurentSettings(self):
        return self.__curInstSettings.items()

    def setInstrument(self, instrumentName):
        self.currentInstrument = instrumentName
        index = self.getInstrumentList().index(self.currentInstrument)
        self.__midiMaster.midiOut.sendProgramChange(index)
        self.__loadCurrentSettings()
        for handler in self.__instrumentUpdateHandlers:
            handler(instrumentName)

    def setInstrumentSetting(self, settingName, value):
      #  val = value / 100.0
        self.__curInstSettings[settingName] = float(value)
        self.__midiMaster.sendControlOutputForControlName(settingName, self.__scaleTo0To100ForControlName(value, settingName))
    
    def getControlRangeData(self, controlName):
        data = self.__instrumentParamsData[controlName]
        start = float(data["start_value"])
        stop = float(data["stop_value"])
        return [start, stop]

    def __filterInstrumentData(self, instrumentData, paramData):
        filteredDict = {}
        namesToUse = ({k:v for (k,v) in paramData.items() if v["type"] == "range"}).keys()
        for instName,controlData in instrumentData.items():
            filteredData = {k: controlData[k] for k in namesToUse if k in controlData.keys() }
            filteredDict[instName] = filteredData

        return filteredDict

    def __loadCurrentSettings(self):
        self.__curInstSettings = copy.deepcopy(self.instrumentData[self.currentInstrument])
        for key, value in self.__curInstSettings.items():
            self.__curInstSettings[key] = float(value)
            self.setInstrumentSetting(key,value)

    def __scaleTo0To100ForControlName(self, val, name):
        low = float(self.__instrumentParamsData[name]["start_value"])
        high = float(self.__instrumentParamsData[name]["stop_value"])
        value = float(val)
        if value < low:
            value = low
            print(f"{val} below low range of {low}")
        elif value > high:
            value = high
            print(f"{val} above high range of {high}")
        return ((value-low) / (high - low)) * 100

    def __scaleToExpectedRangeFrom0To100(self, val, name):
        low = float(self.__instrumentParamsData[name]["start_value"])
        high = float(self.__instrumentParamsData[name]["stop_value"])
        value = float(val)
        
        return (((high - low) / 100)*value) + low

    def midiInHandler(self, controlName, value):
        self.__curInstSettings[controlName] = self.__scaleToExpectedRangeFrom0To100(value, controlName)
        print(self.__curInstSettings[controlName])
        for handler in self.__midiUpdateHandlers:
            handler(controlName, self.__curInstSettings[controlName])



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

with open(instrumentParamsPath, 'r') as reader:
    instrumentParamsData = json.load(reader)

midiMaster = MidiMaster(midiControlData, midiInSubstring, midiOutSubstring)
instruments = Instruments(instrumentData, instrumentParamsData, "piano", midiMaster)

root = Tk() 
root.wm_attributes('-type', 'splash')
root.geometry(f"{windowWidth}x{windowHeight}")

main = MainFrame(root)
main.pack(side="top", fill="both", expand=True)

mainloop() 
