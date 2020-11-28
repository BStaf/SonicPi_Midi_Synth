from tkinter import * 
from tkinter import ttk  
import tkinter.font as tkFont
import mido

instrumentList = [
    "piano", 
    "prophet", 
    "blade",
    "tb303",
    "mod_fm"]

class MidiOut:
    def __init__(self):
        ports = mido.get_output_names()
        print(ports)
        self.midiOut = mido.open_output(ports[1])
        #self.midiOut = mido.open_output('Control Midi Port', virtual=True)

    def sendCmd(self, index):
        msg = mido.Message('program_change', program =index)
        self.midiOut.send(msg)



midiOut = MidiOut()

def InstrumentComboBoxCallback(eventObject):
    index = instrumentList.index(eventObject.widget.get())
    print(index)
    midiOut.sendCmd(index)

root = Tk()      
root.geometry("480x320")
bigfont = tkFont.Font(family="Helvetica",size=17)
root.option_add("*Font", bigfont)
canvas = Canvas(root, width = 480, height = 320)    

cbox = ttk.Combobox(root, justify='center', values=instrumentList,width=20)
cbox.current(0)
cbox.place(x=97, y=7)


cbox.bind("<<ComboboxSelected>>", InstrumentComboBoxCallback)

canvas.pack()
img = PhotoImage(file="guiMain.png")      
canvas.create_image(0,0, anchor=NW, image=img)    
     
  
mainloop() 

