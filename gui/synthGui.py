from tkinter import * 
from tkinter import ttk  
import tkinter.font as tkFont
import mido
import os

guiPicName = os.path.dirname(os.path.realpath(__file__)) + "/guiMain.png"

instrumentList = [
    "piano", 
    "prophet", 
    "blade",
    "tb303",
    "mod_fm"]

class MidiOut:
    def __init__(self):
        print(os.getcwd())
        print(sys.path[0])
        port = [x for x in mido.get_output_names() if "Midi Through" in x][0]
        self.midiOut = mido.open_output(port)

    def sendCmd(self, index):
        msg = mido.Message('program_change', program =index)
        self.midiOut.send(msg)



midiOut = MidiOut()

def InstrumentComboBoxCallback(eventObject):
    index = instrumentList.index(eventObject.widget.get())
    print(index)
    midiOut.sendCmd(index)

root = Tk()      
root.wm_attributes('-type', 'splash')
root.geometry("480x320")
bigfont = tkFont.Font(family="Helvetica",size=17)
root.option_add("*Font", bigfont)
canvas = Canvas(root, width = 480, height = 320)    

cbox = ttk.Combobox(root, justify='center', values=instrumentList,width=20)
cbox.current(0)
cbox.place(x=97, y=7)


cbox.bind("<<ComboboxSelected>>", InstrumentComboBoxCallback)

canvas.pack()
img = PhotoImage(file=guiPicName)      
canvas.create_image(0,0, anchor=NW, image=img)    
     
  
mainloop() 

