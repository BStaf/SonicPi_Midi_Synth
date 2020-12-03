from tkinter import * 
from tkinter import ttk  
from SliderControl import *
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
        print(os.getcwd())
        print(sys.path[0])
        port = [x for x in mido.get_output_names() if "Midi Through" in x][0]
        self.midiOut = mido.open_output(port)
        #self.midiOut = mido.open_output(mido.get_output_names()[1])

    def sendProgramChange(self, index):
        msg = mido.Message('program_change', program =index)
        self.midiOut.send(msg)

    def sendControlChange(self, cntrlId, value):
        msg = mido.Message('control_change', channel=1, control=cntrlId, value=value)
        self.midiOut.send(msg)



midiOut = MidiOut()

def InstrumentComboBoxCallback(eventObject):
    index = instrumentList.index(eventObject.widget.get())
    print(index)
    midiOut.sendProgramChange(index)

def updatePitch(event):
    adjustedVal = 127-event
    midiOut.sendControlChange(20,adjustedVal)

def updateModulation(event):
    midiOut.sendControlChange(21,event)

def updateMasterVolume(event):
    midiOut.sendControlChange(22,event)

root = Tk()      
root.wm_attributes('-type', 'splash')
root.geometry("480x320")
bigfont = tkFont.Font(family="Helvetica",size=17)
root.option_add("*Font", bigfont)
canvas = Canvas(root, width = 480, height = 320)    

cbox = ttk.Combobox(root, justify='center', values=instrumentList,width=20)
cbox.current(0)
cbox.place(x=97, y=7)


cbox.bind("<<ComboboxSelected>>", InstrumentComboBoxCallback)


img = PhotoImage(file=guiPicName)      
canvas.create_image(0,0, anchor=NW, image=img)    
#PitchSldr = SliderControl(canvas,20,70,45,230,0,127,127/2)
PitchSldr = SpringMidiSliderControl(canvas,20,70,127/2)
ModulationSldr = StandardMidiSliderControl(canvas,90,70,0)
MasterVolumeSldr = StandardMidiSliderControl(canvas,415,70,0.9*127)
PitchSldr.OnUpdate(updatePitch)
ModulationSldr.OnUpdate(updateModulation)
MasterVolumeSldr.OnUpdate(updateMasterVolume)
canvas.pack()
  
mainloop() 

