from tkinter import * 
from tkinter import ttk 
from widgets.AppWidgets import *
from AppPalette import *

class NextPage(Frame):
    def __init__(self, pages, instrumentData, midiMaster, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.config(bg=AppPalette.Blue)
        self.__curInstrument = "piano"
        self._sliders = {}
        self.__pages = pages
        self.__midiMaster = midiMaster
        midiMaster.onUpdate(self.midiInHandler)
        self.__instrumentData = instrumentData
        self.__canvasTop = Canvas(self, width=self['width'], height=50, bg=AppPalette.DarkBlue,highlightthickness=0) 
        self.__canvasBottom = Canvas(self, width=self['width'], height=self['height']-50, bg=AppPalette.Blue,highlightthickness=0)  

        self.__populateTopCanvas(self.__canvasTop)
        self.__populateBottomCanvas(self.__canvasBottom)

        self.__canvasTop.pack(side="top", expand=YES)
        self.__canvasBottom.pack(side="bottom", expand=YES)#3fill=BOTH, expand=YES)

    def show(self, instrument):
        self.setInstrument(instrument)
        self.lift()

    def setInstrument(self, instrument):
        self.__curInstrument = instrument
        self.__populateBottomCanvas(self.__canvasBottom)

    def midiInHandler(self, controlName, value):
        #print(f"NextPage midiInHandler-{controlName}-{value}")
        slider = self._sliders.get(controlName, None)
        if slider is not None:
            slider.setToValue(value)

    def __btnCallback(self, event):
        self.__pages["mainPage"].show()

    def __populateTopCanvas(self, canvas):
        titleLbl = Label(canvas, text="SP1X")
        titleLbl.config(fg=AppPalette.White, bg=AppPalette.DarkBlue, font='Helvetica 28 bold')
        titleLbl.place(x=275, y=25,  anchor="center")

        MenuBtn(canvas, 20, 10, 120, 30, "Back", self.__btnCallback)

    def __populateBottomCanvas(self, canvas):
        
        self.__canvasBottom.delete("all")
        #draw new sliders
        i = 0
        for name, value in self.__instrumentData[self.__curInstrument].items():
            if i > 4:
                break
            lbl = LowerLabel(canvas, text=name)
            lbl.place(x = (i*75)+45,y = 13, anchor="center")
            xPos = (i*75)+20
            slider = StandardMidiSliderControl(canvas,xPos,26,float(value)*100)
            slider.OnUpdate(self.__handleSliderChange)
            self._sliders[name] = slider
            i = i+1

    def __handleSliderChange(self, obj, event):
        for key, value in self._sliders.items():
            if value == obj:
                #print (f"Found {key}, {event}")
                self.__midiMaster.sendControlOutputForControlName(key, event)