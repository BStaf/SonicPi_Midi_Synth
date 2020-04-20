# from tkinter import *


# gui = Tk()

# gui.geometry("480x320")
# #set window color
# gui.configure(bg='#0F4470')

# w = Canvas(gui, width=200, height=100)
# w.pack()

# w.create_line(0, 0, 200, 100)
# w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

# w.create_rectangle(50, 25, 150, 75, fill="blue")

# mainloop()

# # master = Tk()

# # frame = Frame(master)
# # scrollbar = Scrollbar(frame, orient=VERTICAL)
# # listbox = Listbox(master, yscrollcommand=scrollbar.set)
# # scrollbar.config(command=listbox.yview)
# # scrollbar.pack(side=RIGHT, fill=Y)
# # listbox.pack(side=LEFT, fill=BOTH, expand=1)
# # frame.pack()

# # listbox.insert(END, "a list entry")

# # for item in ["one", "two", "three", "four","sadf","asdf","weqerw","asfcv","sadfqewf","tyujnvb","aewrcv"]:
# #     listbox.insert(END, item)

# # mainloop()
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
# pip install pillow
from PIL import Image, ImageTk
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class SynthHandler():

    instruments = {"piano": 1, "prophit": 2}
    curInstrument = ""
    def __init__(self):
        self.curInstrument = "piano"
    
    def GetCurrentInstrument(self):
        return (self.curInstrument, self.instruments[self.curInstrument])

    def SetInstrument(instrument):
        curInstrument = instrument
        #return ''

Synth = SynthHandler()

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("960x640")
        
       # mainFrame = 



        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=960, height=640)
        self.controller = controller
        self.pack()
        #set window color
        #self.configure(bg='#0F4470')
        self.setupBackgroundImage("guiMain.jpg")
        label = tk.Label(self, text=Synth.GetCurrentInstrument(), font=controller.title_font)
        label.place(relx=200.5, rely=200.5, anchor = tk.CENTER)
        #label.pack(side="top", fill="x", pady=10)
        label.pack()
        # button1 = tk.Button(self, text="Go to Page One",
        #                     command=lambda: controller.show_frame("PageOne"))
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()
    
    def setupBackgroundImage(self,imageName):
        load = Image.open(imageName)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    
    print (Synth.GetCurrentInstrument())
    app = SampleApp()
    app.mainloop()