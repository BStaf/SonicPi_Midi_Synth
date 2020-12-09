from subprocess import call
from tkinter import * 
from tkinter import ttk 
from widgets.AppWidgets import *
from AppPalette import *

class MainPage(Frame):
    def __init__(self, pages, instrumentList, midiMaster, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.config(bg=AppPalette.Blue)
        self.__curInstrument = "piano"
        self.__midiMaster = midiMaster
        self.__pages = pages
        self.instrumentList = instrumentList
        canvasTop = Canvas(self, width=self['width'], height=50, bg=AppPalette.DarkBlue,highlightthickness=0) 
        canvasBottom = Canvas(self, width=self['width'], height=self['height']-50, bg=AppPalette.Blue,highlightthickness=0)  

        self.populateTopCanvas(canvasTop)
        self.populateBottomCanvas(canvasBottom)

        canvasTop.pack(side="top", expand=YES)
        canvasBottom.pack(side="bottom", expand=YES)#3fill=BOTH, expand=YES)

    def show(self):
        self.lift()

    def btnCallback(self, event):
        self.__pages["instConfigPage"].show(self.__curInstrument)

    def shutdownCallback(self, event):
        call("sudo shutdown -h now", shell=True)

    def populateTopCanvas(self, canvas):
        titleLbl = Label(canvas, text="SP1X")
        titleLbl.config(fg=AppPalette.White, bg=AppPalette.DarkBlue, font='Helvetica 28 bold')
        titleLbl.place(x=275, y=25,  anchor="center")
        MenuBtn(canvas, 20, 10, 120, 30, "Next", self.btnCallback)
        MenuBtn(canvas, 408, 10, 50, 30, "X", self.shutdownCallback)
        return

    def populateBottomCanvas(self, canvas):
        cbox = ttk.Combobox(canvas, justify='center', values=self.instrumentList,width=15, height=7)
        cbox.config(font='Helvetica 17')
        cbox.current(0)
        cbox.place(x=170, y=26)
        cbox.bind("<<ComboboxSelected>>", self.instrumentComboBoxCallback)

        PitchSldr = SpringMidiSliderControl(canvas, 20,26,50)
        ModulationSldr = StandardMidiSliderControl(canvas, 90,26,0)
        MasterVolumeSldr = StandardMidiSliderControl(canvas, 408,26,90)

        PitchSldr.OnUpdate(self.updatePitch)
        ModulationSldr.OnUpdate(self.updateModulation)
        MasterVolumeSldr.OnUpdate(self.updateMasterVolume)
        
        lblPitch = LowerLabel(canvas, text='Pitch')
        lblPitch.place(x = 43,y = 13, anchor="center")
        lblMod = LowerLabel(canvas, text='Modulation')
        lblMod.place(x = 115,y = 13, anchor="center")
        lblInst = LowerLabel(canvas, text='Instrument')
        lblInst.place(x = 275,y = 13, anchor="center")
        lblVol = LowerLabel(canvas, text='Mstr Volume')
        lblVol.place(x = 432,y = 13, anchor="center")
        return

    def instrumentComboBoxCallback(self, eventObject):
        self.__curInstrument = eventObject.widget.get()
        index = self.instrumentList.index(self.__curInstrument)
        print(index)
        self.__midiMaster.midiOut.sendProgramChange(index)
        return

    def updatePitch(self, obj, event):
        self.__midiMaster.sendControlOutputForControlName("pitch", event)
        return

    def updateModulation(self, obj, event):
        self.__midiMaster.sendControlOutputForControlName("modulation", event)
        return

    def updateMasterVolume(self, obj, event):
        self.__midiMaster.sendControlOutputForControlName("master_volume", event)
        return