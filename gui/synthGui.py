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
midiControlJsonPath = os.path.dirname(os.path.realpath(__file__)) + "/ControlData.Json"

windowHeight = 320
windowWidth = 480


class MidiOut:
    def __init__(self):
        port = [x for x in mido.get_output_names() if "Midi Through" in x][0]
        self.midiOut = mido.open_output(port)
        print(mido.get_output_names())
        self.channel = 15
        #self.midiOut = mido.open_output(mido.get_output_names()[2])

    def sendProgramChange(self, index):
        msg = mido.Message('program_change', channel=self.channel, program =index)
        self.midiOut.send(msg)

    def sendControlChange(self, cntrlId, value):
        #print(f"midi out = {cntrlId} - {value}")
        msg = mido.Message('control_change', channel=self.channel, control=cntrlId, value=value)
        self.midiOut.send(msg)
    
class MidiIn(Thread):
    def __init__(self):
        Thread.__init__(self)
        print(mido.get_input_names())
        self.handlers = []
        port = [x for x in mido.get_input_names() if "Arduino" in x][0] 
        #port = [x for x in mido.get_input_names() if "Midi Through" in x][0]
        self.midiOut = mido.open_input(port)
        #self.midiIn = mido.open_input(mido.get_input_names()[0])

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
    def __init__(self, midiControlData):
        self.__handlers = []
        self.midiOut = MidiOut()
        self.__midiIn = MidiIn()
        self.__midiIn.daemon = True #set this thread as a Daemon Thread
        self.__midiIn.OnUpdate(self.midiInHandler)
        #self.__midiIn.start()

        self.__midiControlData = midiControlData

    def onUpdate(self, handler):
        self.__handlers.append(handler)

    def sendControlOutputForControlName(self,controlName, value):
        controlId = int(self.__midiControlData[controlName]["midi_out_control"])
        midiVal = value/100 * 127
        self.midiOut.sendControlChange(int(controlId), int(midiVal))

    def midiInHandler(self, controlId, value):
        #if controlId is in midiControlData send out event
        for key, dictVal in self.__midiControlData.items():
            #print (f"{controlId}-{value}")
            id = dictVal.get('midi_in_control', None)
            if id is not None and int(id) == controlId:
                controlName = key
                #produce Event
                for handler in self.__handlers:
                    handler(controlName, value)
                break

class MainFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        pages = {}

        pages["instConfigPage"] = NextPage(pages, instrumentData, midiMaster, root, width=windowWidth, height=windowHeight)
        pages["mainPage"] = MainPage(pages, list(instrumentData.keys()), midiMaster, root, width=windowWidth, height=windowHeight)

        container = Frame(self)
        container.pack(fill="both", expand=True)

        for key, value in pages.items():
             value.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        pages["mainPage"].show()
   
with open(instrumentJsonPath, 'r') as reader:
    instrumentData = json.load(reader)

with open(midiControlJsonPath, 'r') as reader:
    midiControlData = json.load(reader)

midiMaster = MidiMaster(midiControlData)

root = Tk() 
root.wm_attributes('-type', 'splash')
root.geometry(f"{windowWidth}x{windowHeight}")
bigfont = tkFont.Font(family="Helvetica",size=17)
root.option_add("*Font", bigfont)


main = MainFrame(root)
main.pack(side="top", fill="both", expand=True)

mainloop() 
