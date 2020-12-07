from tkinter import * 
from tkinter import ttk 
from widgets.AppWidgets import *
from AppPalette import *

class NextPage(Frame):
    def __init__(self, instrumentList, midiOut, midiIn, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.config(bg=AppPalette.Blue)
        self.midiOut = midiOut
        midiIn.OnUpdate(self.midiInHandler)
        self.instrumentList = instrumentList
        canvasTop = Canvas(self, width=self['width'], height=50, bg=AppPalette.DarkBlue,highlightthickness=0) 
        canvasBottom = Canvas(self, width=self['width'], height=self['height']-50, bg=AppPalette.Blue,highlightthickness=0)  

        self.populateTopCanvas(canvasTop)
        self.populateBottomCanvas(canvasBottom)

        canvasTop.pack(side="top", expand=YES)
        canvasBottom.pack(side="bottom", expand=YES)#3fill=BOTH, expand=YES)

    def midiInHandler(self, control, value):
        print(f"Next-{control}-{value}")
        if control == 1:
            self.sldr.setToValue(value)

    def btnCallback(self, event):
        print("called")

    def populateTopCanvas(self, canvas):
        titleLbl = Label(canvas, text="SP1X")
        titleLbl.config(fg=AppPalette.White, bg=AppPalette.DarkBlue, font='Helvetica 28 bold')
        titleLbl.place(x=275, y=25,  anchor="center")

        MenuBtn(canvas, 20, 10, 120, 30, "Next", self.btnCallback)
        MenuBtn(canvas, 408, 10, 50, 30, "X", self.btnCallback)
        return

    def populateBottomCanvas(self, canvas):
        self.sldr = StandardMidiSliderControl(canvas,20,26,0)
        StandardMidiSliderControl(canvas,85,26,0)
        StandardMidiSliderControl(canvas,150,26,0)
        StandardMidiSliderControl(canvas,215,26,0)
        StandardMidiSliderControl(canvas,280,26,0)
        StandardMidiSliderControl(canvas,345,26,0)
        StandardMidiSliderControl(canvas,410,26,0)
        # ModulationSldr = StandardMidiSliderControl(canvas,90,26,0)
        # MasterVolumeSldr = StandardMidiSliderControl(canvas,408,26,0.9*127)

        # ModulationSldr.OnUpdate(self.updateModulation)
        # MasterVolumeSldr.OnUpdate(self.updateMasterVolume)
        
        # lblPitch = LowerLabel(canvas, text='Pitch')
        # lblPitch.place(x = 43,y = 13, anchor="center")
        # lblMod = LowerLabel(canvas, text='Modulation')
        # lblMod.place(x = 115,y = 13, anchor="center")
        # lblInst = LowerLabel(canvas, text='Instrument')
        # lblInst.place(x = 275,y = 13, anchor="center")
        # lblVol = LowerLabel(canvas, text='Mstr Volume')
        # lblVol.place(x = 432,y = 13, anchor="center")
        return

    def instrumentComboBoxCallback(self, eventObject):
        index = self.instrumentList.index(eventObject.widget.get())
        print(index)
        self.midiOut.sendProgramChange(index)
        return

    def updatePitch(self, event):
        self.midiOut.sendControlChange(20,event)
        return

    def updateModulation(self, event):
        self.midiOut.sendControlChange(21,event)
        return

    def updateMasterVolume(self, event):
        self.midiOut.sendControlChange(22,event)
        return