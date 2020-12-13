from subprocess import call
from tkinter import * 
from tkinter import ttk 
from widgets.AppWidgets import *
from AppPalette import *

class MainPage(Frame):
    def __init__(self, pages, instruments, midiMaster, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.config(bg=AppPalette.Blue)

        self.__midiMaster = midiMaster
        self.__pages = pages
        self.__instruments = instruments

        canvasTop = Canvas(self, width=self['width'], height=50, bg=AppPalette.DarkBlue,highlightthickness=0) 
        canvasBottom = Canvas(self, width=self['width'], height=self['height']-50, bg=AppPalette.Blue,highlightthickness=0)  

        self.populateTopCanvas(canvasTop)
        self.populateBottomCanvas(canvasBottom)
        self.__instSelectBtn = MenuBtn(canvasBottom, 184,26, 180, 30, self.__instruments.currentInstrument, self.btnCallBackInstSelect)
        canvasTop.pack(side="top", expand=YES)
        canvasBottom.pack(side="bottom", expand=YES)#3fill=BOTH, expand=YES)

    def show(self):
        self.__instSelectBtn.changeLable(self.__instruments.currentInstrument)
        self.lift()

    def btnCallbackInstConfig(self, event):
        self.__pages["instConfigPage"].show()

    def btnCallBackInstSelect(self, event):
        self.__pages["instSelectPage"].show()

    def shutdownCallback(self, event):
        call("sudo shutdown -h now", shell=True)

    def populateTopCanvas(self, canvas):
        titleLbl = Label(canvas, text="SP1X")
        titleLbl.config(fg=AppPalette.White, bg=AppPalette.DarkBlue, font='Helvetica 28 bold')
        titleLbl.place(x=275, y=25,  anchor="center")
        MenuBtn(canvas, 20, 10, 120, 30, "Settings", self.btnCallbackInstConfig)
        MenuBtn(canvas, 408, 10, 50, 30, "X", self.shutdownCallback)
        return

    def populateBottomCanvas(self, canvas):
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
        
    def updatePitch(self, obj, event):
        self.__midiMaster.sendControlOutputForControlName("pitch", event)
        return

    def updateModulation(self, obj, event):
        self.__midiMaster.sendControlOutputForControlName("modulation", event)
        return

    def updateMasterVolume(self, obj, event):
        self.__midiMaster.sendControlOutputForControlName("master_volume", event)
        return