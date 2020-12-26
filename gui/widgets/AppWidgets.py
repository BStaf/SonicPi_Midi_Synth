from tkinter import *
from AppPalette import *
from widgets.SliderControl import *

class LowerLabel(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self.config(fg=AppPalette.White, bg=AppPalette.Blue)
        #lblPitch.place(x = 43,y = 67, anchor="center")
        self.config(font='Times 10 bold')

class Btn:
    def __init__(self, canvas, x, y, width, height, text, fontSize, callBack):
        btnRect = canvas.create_rectangle(x, y, x+width, y+height, fill=AppPalette.Black)
        self._btnLbl = Label(canvas, text=text)
        self._btnLbl.config(fg=AppPalette.White, bg=AppPalette.Black, font=f"Helvetica {fontSize} bold")
        self._btnLbl.place(x=x+(width/2),y=y+(height/2), anchor="center")

        self._callBack = callBack
    
        canvas.tag_bind(btnRect, '<Button-1>', self._btnCallback)
        self._btnLbl.bind("<Button-1>", self._btnCallback)

    def _btnCallback(self, event):
        self._callBack(event)

    def changeLable(self, text):
        self._btnLbl.config(text = text)


class MenuBtn(Btn):
    def __init__(self, canvas, x, y, width, height, text, callBack):
        Btn.__init__(self,canvas, x, y, width, height, text, 12, callBack)
    

class InstrumentSelectBtn(Btn):
    def __init__(self, canvas, x, y, width, height, text, callBack):
        Btn.__init__(self,canvas, x, y, width, height, text, 9, callBack)
        self._callBack = callBack
        self._text = text

    def _btnCallback(self, event):
        self._callBack(event, self._text)


class StandardMidiSliderControl(SliderControl):
    def __init__(self, canvas, xPos, yPos, minVal, maxVal, startVal):
        SliderControl.__init__(self, canvas, xPos, yPos, 50, 230, minVal, maxVal, startVal) 

#reverts to startVal when let go
class SpringMidiSliderControl(StandardMidiSliderControl):
    def __init__(self, canvas, xPos, yPos, startVal):
        StandardMidiSliderControl.__init__(self, canvas, xPos, yPos, 0, 100, startVal)
        self.beginVal = self._startYPos+self._sliderHalfHeight
        canvas.tag_bind(self._slider, '<ButtonRelease-1>', self.btnUp) 

    def btnUp(self, event):
        self._updateSlider(self.beginVal)
        self._updateSliderValue(self.beginVal)
        return