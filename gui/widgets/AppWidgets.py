from tkinter import *
from AppPalette import *

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