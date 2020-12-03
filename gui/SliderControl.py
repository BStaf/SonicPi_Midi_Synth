from tkinter import *

class SliderControl:
    def __init__(self, canvas, xPos, yPos, width, height, minVal, maxVal, startVal):
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

        sliderYPos = self.sliderRange - ( (startVal / (self.maxVal-self.minVal)) * self.sliderRange ) + yPos
       
        #self.slider = canvas.create_rectangle(xPos, yPos, width, width, fill="yellow")
        self.rect = canvas.create_rectangle(xPos, yPos, xPos+width, yPos+height, fill="#232628")
        
        self.slider = canvas.create_rectangle(xPos, sliderYPos, xPos+width, sliderYPos+sliderHeight, fill="#FFBE31")
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
        percent = 1 - (curPosY1 / self.sliderRange)
        return int((percent * (self.maxVal-self.minVal)) + self.minVal)

    def getSliderMovementValue(self, yPos):
        #get current slider position
        curPosY1 = self.canvas.coords(self.slider)[1] - self.objectYpos
        curPosY2 = self.canvas.coords(self.slider)[3] - self.objectYpos
        #get move value
        posDif = yPos - self.lastYpos
        self.lastYpos = yPos
        #disable overrun      
        if curPosY1+posDif < 0: posDif = 0 - curPosY1
        if curPosY2+posDif > self.height: posDif = self.height - curPosY2

        return posDif

# def update(event):
#    print(event)


# root = Tk()
# windowWidth = 480
# windowHeight = 320   
# root.geometry(f"{windowWidth}x{windowHeight}")
# C = Canvas(root, height=windowHeight, width=windowWidth)
# x = 10
# y = 50
# width = 50
# height = 200
# slider1 = SliderControl(C,x,y,width,height,0,127)
# slider1.OnUpdate(update)
# C.pack()
# root.mainloop()