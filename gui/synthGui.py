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
        #print(os.getcwd())
        #print(sys.path[0])
        #port = [x for x in mido.get_output_names() if "Midi Through" in x][0]
        #self.midiOut = mido.open_output(port)
        self.midiOut = mido.open_output(mido.get_output_names()[1])

    def sendProgramChange(self, index):
        msg = mido.Message('program_change', program =index)
        self.midiOut.send(msg)

    def sendControlChange(self, cntrlId, value):
        msg = mido.Message('control_change', channel=1, control=cntrlId, value=value)
        self.midiOut.send(msg)

class MainPage(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        canvas = Canvas(self, bg="#0F4470")  

        canvas.create_rectangle(0, 0, 480 , 60 , fill="#232628")

        cbox = ttk.Combobox(self, justify='center', values=instrumentList,width=15)
        cbox.current(0)
        cbox.place(x=170, y=15)
        cbox.bind("<<ComboboxSelected>>", self.instrumentComboBoxCallback)

        PitchSldr = SpringMidiSliderControl(canvas,20,55,63)
        ModulationSldr = StandardMidiSliderControl(canvas,90,70,0)
        MasterVolumeSldr = StandardMidiSliderControl(canvas,415,70,0.9*127)

        PitchSldr.OnUpdate(self.updatePitch)
        ModulationSldr.OnUpdate(self.updateModulation)
        MasterVolumeSldr.OnUpdate(self.updateMasterVolume)
        
        lbl = Label(canvas, text='Pitch', fg="#FFF5F7", bg="#232628")
        lbl.place(x = 40,y = 35, anchor="center")
        lbl.config(font='Helvetica 10 bold')
        lbl.pack
        canvas.pack(fill=BOTH, expand=YES)
        
    def instrumentComboBoxCallback(self, eventObject):
        index = instrumentList.index(eventObject.widget.get())
        print(index)
        midiOut.sendProgramChange(index)

    def updatePitch(self, event):
        midiOut.sendControlChange(20,event)

    def updateModulation(self, event):
        midiOut.sendControlChange(21,event)

    def updateMasterVolume(self, event):
        midiOut.sendControlChange(22,event)


midiOut = MidiOut()

def InstrumentComboBoxCallback(eventObject):
    index = instrumentList.index(eventObject.widget.get())
    print(index)
    midiOut.sendProgramChange(index)

def updatePitch(event):
    midiOut.sendControlChange(20,event)

def updateModulation(event):
    midiOut.sendControlChange(21,event)

def updateMasterVolume(event):
    midiOut.sendControlChange(22,event)

root = Tk()      
#root.wm_attributes('-type', 'splash')
windowHeight = 320
windowWidth = 480
root.geometry(f"{windowWidth}x{windowHeight}")

bigfont = tkFont.Font(family="Helvetica",size=17)
root.option_add("*Font", bigfont)

main = MainPage(root)
main.pack(fill="both", expand=True)
# canvas = Canvas(root)#, width = 480, height = 320)    

# cbox = ttk.Combobox(root, justify='center', values=instrumentList,width=20)
# cbox.current(0)
# cbox.place(x=97, y=7)


# cbox.bind("<<ComboboxSelected>>", InstrumentComboBoxCallback)


# img = PhotoImage(file=guiPicName)      
# canvas.create_image(0,0, anchor=NW, image=img)    

# PitchSldr = SpringMidiSliderControl(canvas,20,70,63)
# ModulationSldr = StandardMidiSliderControl(canvas,90,70,0)
# MasterVolumeSldr = StandardMidiSliderControl(canvas,415,70,0.9*127)
# PitchSldr.OnUpdate(updatePitch)
# ModulationSldr.OnUpdate(updateModulation)
# MasterVolumeSldr.OnUpdate(updateMasterVolume)
# canvas.pack(fill=BOTH, expand=YES)
  
mainloop() 

