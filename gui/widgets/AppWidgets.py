from tkinter import *
from AppPalette import *
from widgets.SliderControl import *

class LowerLabel(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self.config(fg=AppPalette.White, bg=AppPalette.Blue)
        #lblPitch.place(x = 43,y = 67, anchor="center")
        self.config(font='Times 10 bold')

class MenuBtn:
    def __init__(self, canvas, x, y, width, height, text, callBack):
        btnRect = canvas.create_rectangle(x, y, x+width, y+height, fill=AppPalette.Black)
        btnLbl = Label(canvas, text=text)
        btnLbl.config(fg=AppPalette.White, bg=AppPalette.Black, font='Helvetica 12 bold')
        btnLbl.place(x=x+(width/2),y=y+(height/2), anchor="center")

        canvas.tag_bind(btnRect, '<Button-1>', callBack)
        btnLbl.bind("<Button-1>", callBack)

class StandardMidiSliderControl(SliderControl):
    def __init__(self, canvas, xPos, yPos, startVal):
        SliderControl.__init__(self, canvas, xPos, yPos, 50, 230, 0 , 100, startVal) 

#reverts to startVal when let go
class SpringMidiSliderControl(StandardMidiSliderControl):
    def __init__(self, canvas, xPos, yPos, startVal):
        StandardMidiSliderControl.__init__(self, canvas, xPos, yPos, startVal)
        self.beginVal = self._startYPos+self._sliderHalfHeight
        canvas.tag_bind(self._slider, '<ButtonRelease-1>', self.btnUp) 

    def btnUp(self, event):
        self._updateSlider(self.beginVal)
        self._updateSliderValue(self.beginVal)
        return