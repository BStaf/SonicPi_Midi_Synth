from tkinter import * 
from tkinter import ttk 
from widgets.AppWidgets import *
from AppPalette import *

class InstSettingsPage(Frame):
    def __init__(self, pages, instruments, midiMaster, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.config(bg=AppPalette.Blue)
        self.__instruments = instruments
        self.__instruments.onMidiInUpdate(self.midiInHandler)
        self.__instruments.onInstrumentUpdate(self.instrumentChangeHandler)

        self._sliders = {}
        self._sliderLabels = []
        self.__pages = pages

        self.__midiMaster = midiMaster
        #self.__midiMaster.onUpdate(self.midiInHandler)
        
        self.__canvasTop = Canvas(self, width=self['width'], height=50, bg=AppPalette.DarkBlue,highlightthickness=0) 
        self.__canvasBottom = Canvas(self, width=self['width'], height=self['height']-50, bg=AppPalette.Blue,highlightthickness=0)  

        self.__setupForNewInstrument(self.__instruments.currentInstrument)

        self.__populateTopCanvas(self.__canvasTop)
        self.__populateBottomCanvas(self.__canvasBottom)

        self.__canvasTop.pack(side="top", expand=YES)
        self.__canvasBottom.pack(side="bottom", expand=YES)#3fill=BOTH, expand=YES)

    def show(self):
        self.__updateAllSliders()
        #self.__populateBottomCanvas(self.__canvasBottom)
        self.lift()

    def midiInHandler(self, controlName, value):
        #print(f"NextPage midiInHandler-{controlName}-{value}")
        slider = self._sliders.get(controlName, None)

        if slider is not None:
            slider.setToValue(value)

    def instrumentChangeHandler(self, instrumentName):
        self.__setupForNewInstrument(instrumentName)
        self.__populateBottomCanvas(self.__canvasBottom)

    def __setupForNewInstrument(self, instrumentName):
        self.__sliderCount = len(self.__instruments.getCurentSettings())
        self.__slidersPos = 0

    def __btnCallback(self, event):
        self.__pages["mainPage"].show()

    def __settingsShiftLeftCallback(self, event):    
        newSlidersPos = self.__slidersPos + 2
        #5 is the number of sliders eveer on the screen
        if (newSlidersPos + 5) >= self.__sliderCount:
            newSlidersPos = self.__sliderCount - 5
        self.__moveSliders(newSlidersPos, -1)
       
    def __settingsShiftRightCallback(self, event):    
        newSlidersPos = self.__slidersPos - 2
        #5 is the number of sliders eveer on the screen
        if newSlidersPos < 0:
            newSlidersPos = 0
        self.__moveSliders(newSlidersPos, 1)

    def __moveSliders(self, newSlidersPos, directionMultiplier):
        sliderSpacing = 75
        dif = -(newSlidersPos - self.__slidersPos) * sliderSpacing #* directionMultiplier    
        #print(f"Cur pos: {self.__slidersPos} New pos: {newSlidersPos} Dif: {dif}")
        for slider in self._sliders.values():
            slider.moveHorizontally(dif)
        labelNames = list(self._sliders.keys())
        i=0
        for lbl in self._sliderLabels:
            lbl.config(text = labelNames[i+newSlidersPos])
            i = i+1
            #curXPos = int(lbl.winfo_x()+(lbl.winfo_width()/2))
            #lbl.place(x=curXPos+dif)
        self.__slidersPos = newSlidersPos

    def __populateTopCanvas(self, canvas):
        titleLbl = Label(canvas, text="SP1X")
        titleLbl.config(fg=AppPalette.White, bg=AppPalette.DarkBlue, font='Helvetica 28 bold')
        titleLbl.place(x=275, y=25,  anchor="center")

        MenuBtn(canvas, 20, 10, 120, 30, "Back", self.__btnCallback)

    def __populateBottomCanvas(self, canvas):
        sliderStartXPos = 60
        sliderSpacing = 75

        #remove existing sliders and labels
        self.__canvasBottom.delete("all")
        self._sliders.clear()       
        for lbl in self._sliderLabels:
            lbl.destroy()
        self._sliderLabels.clear()

        #draw sliders
        i = 0
        print("slides for")
        print(self.__instruments.getCurentSettings())
        for name, value in self.__instruments.getCurentSettings():
            print(f"{name}-{value}")
            if i < 5:
                lbl = LowerLabel(canvas, text=name)
                lbl.place(x = (i*sliderSpacing)+sliderStartXPos+25,y = 13, anchor="center")
                self._sliderLabels.append(lbl)
            xPos = (i*sliderSpacing)+sliderStartXPos
            
            rangeData = self.__instruments.getControlRangeData(name)
            #print(f"rangeData is {rangeData}")
            slider = StandardMidiSliderControl(canvas, xPos, 26, rangeData[0], rangeData[1], float(value))
            slider.OnUpdate(self.__handleSliderChange)
            self._sliders[name] = slider          
            i = i+1
        print("done")
        canvas.create_rectangle(0, 0, 50, 300, fill=AppPalette.Blue, outline="")
        canvas.create_rectangle(430, 0, 430+50, 300, fill=AppPalette.Blue, outline="")
        MenuBtn(canvas, 10, 66, 30, 150, "<", self.__settingsShiftRightCallback)
        MenuBtn(canvas, 435, 66, 30, 150, ">", self.__settingsShiftLeftCallback)
        
        
    def __updateAllSliders(self):
        i = 0
        for name, value in self.__instruments.getCurentSettings():
            if i > 4:
                break
            slider = self._sliders.get(name, None)

            if slider is not None:
                slider.setToValue(float(value))

    def __handleSliderChange(self, obj, event):
        for key, value in self._sliders.items():
            if value == obj:
                #print (f"Found {key}, {event}")
                self.__instruments.setSetting(key, event)
                #self.__midiMaster.sendControlOutputForControlName(key, event)