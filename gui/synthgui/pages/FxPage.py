from subprocess import call
from tkinter import * 
from tkinter import ttk 
from widgets.AppWidgets import *
from AppPalette import *

class FxPage(Frame):
    def __init__(self, pages, fxs, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.config(bg=AppPalette.Blue)
        self.__pages = pages
        self.__fxs = fxs
        canvasTop = Canvas(self, width=self['width'], height=50, bg=AppPalette.DarkBlue,highlightthickness=0) 
        canvasBottom = Canvas(self, width=self['width'], height=self['height'], bg=AppPalette.Blue,highlightthickness=0)  

        self.populateTopCanvas(canvasTop)
        self.populateBottomCanvas(canvasBottom)

        canvasTop.pack(side="top", expand=YES)
        canvasBottom.pack(side="bottom", expand=YES)

    def show(self):
        self.lift()

    def backBtnCallback(self, event):
        self.__pages["mainPage"].show()
    
    def fxSelectBtnCallback(self, event, name):
        print(name)
        self.__fxs.setCurrent(name)
        self.__pages["fxConfigPage"].show()

    def populateTopCanvas(self, canvas):
        titleLbl = Label(canvas, text="SP1X")
        titleLbl.config(fg=AppPalette.White, bg=AppPalette.DarkBlue, font='Helvetica 28 bold')
        titleLbl.place(x=275, y=25,  anchor="center")
        MenuBtn(canvas, 20, 10, 120, 30, "Back", self.backBtnCallback)
        return

    def populateBottomCanvas(self, canvas):
        #draw new sliders
        i = 0
        j = 0
        for fxName in self.__fxs.getList():
            InstrumentSelectBtn(canvas, i*90+10, j*40+10, 80, 30, fxName, self.fxSelectBtnCallback)

            j = j+1
            if j > 5:
                j=0
                i = i+1
        return
