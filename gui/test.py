from tkinter import *

class SliderRectangle:
    def __init__(self, canvas, xPos, yPos, width, height, minVal, maxVal):
        self.handlers = []
        self.canvas = canvas
        self.objectYpos = yPos
        self.height = height
        self.minVal = minVal
        self.maxVal = maxVal
        
        sliderHeight = width/1.5
        self.sliderRange = height-sliderHeight

        self.lastYpos=0
        self.lastVal=0

        #self.slider = canvas.create_rectangle(xPos, yPos, width, width, fill="yellow")
        self.rect = canvas.create_rectangle(xPos, yPos, xPos+width, yPos+height, fill="black")
        
        self.slider = canvas.create_rectangle(xPos, yPos, xPos+width, yPos+sliderHeight, fill="yellow")
        canvas.tag_bind(self.slider, '<B1-Motion>',self.motion) 
        canvas.tag_bind(self.slider, '<Button-1>', self.btnDown)

    def OnUpdate(self, handler):
        self.handlers.append(handler)
        return

    def btnDown(self, event):
        self.lastYpos = event.y
        return

    def motion(self, event):
        posDif = self.getSliderMovementValue(event.y)
        #draw slider
        self.canvas.move(self.slider, 0, posDif)
        self.canvas.update()
        #get updated slider value
        val = self.calcCurrentPosValue(event.y)
        #print (f"curent value is {val}")
        if val != self.lastVal:
            for handler in self.handlers:
                handler(val)
        self.lastVal = val
        return

    def calcCurrentPosValue(self, yPos):
        #get latest slider position
        curPosY1 = self.canvas.coords(self.slider)[1] - self.objectYpos
        return int(((curPosY1 / self.sliderRange) * (self.maxVal-self.minVal)) + self.minVal)

    def getSliderMovementValue(self, yPos):
        #get current slider position
        curPosY1 = self.canvas.coords(self.slider)[1] - self.objectYpos
        curPosY2 = self.canvas.coords(self.slider)[3] - self.objectYpos
        #get move value
        posDif = yPos - self.lastYpos
        self.lastYpos = yPos
        #disable overrun      
        if curPosY1+posDif < 0: posDif = 0 - curPosY1
        if curPosY2+posDif > self.height: posDif = height - curPosY2

        return posDif

def update(event):
    print(event)
# def motion(event):
#    print("Mouse position: (%s %s)" % (event.x, event.y))
#    return

# master = Tk()
# whatever_you_do = "Whatever you do will be insignificant, but it is very important that you do it.\n(Mahatma Gandhi)"
# msg = Message(master, text = whatever_you_do)
# msg.config(bg='lightgreen', font=('times', 24, 'italic'))
# msg.bind('<Motion>',motion)
# msg.pack()
# mainloop()

root = Tk()
windowWidth = 480
windowHeight = 320   
root.geometry(f"{windowWidth}x{windowHeight}")
#C = Canvas(root, bg="blue", height=250, width=300)
C = Canvas(root, height=windowHeight, width=windowWidth)
#C.place(x=5, y=7)
#coord = 10, 50, 240, 210
x = 10
y = 50
width = 50
height = 200
#rect = C.create_rectangle(x, y, x+wdith, y+height, fill="black")
slider1 = SliderRectangle(C,x,y,width,height,0,127)
slider1.OnUpdate(update)
#arc = C.create_arc(coord, start=0, extent=150, fill="red")
#arc.bind('<Motion>',motion)
#C.tag_bind(rect, '<Motion>',motion) 
C.pack()
root.mainloop()