from tkinter import *
from AppPalette import *

class SliderControl:
    def __init__(self, canvas, xPos, yPos, width, height, minVal, maxVal, startVal):
        self.__handlers = []
        self.__canvas = canvas
        self._objectYpos = yPos
        self._height = height
        self._minVal = minVal
        self._maxVal = maxVal
        self.__yPos = yPos
        
        sliderHeight = width/1.3
        self._sliderHalfHeight = sliderHeight/2
        print(f"{sliderHeight}-{self._sliderHalfHeight+sliderHeight}-{yPos}-{yPos+self._sliderHalfHeight}")
        self._sliderRange = height-sliderHeight

        #self.lastYpos=0
        self._lastVal=0

        self._startYPos = self._sliderRange - ( (startVal / (self._maxVal-self._minVal)) * self._sliderRange ) + yPos
       
        canvas.create_rectangle(xPos, yPos, xPos+width, yPos+height, fill=AppPalette.Black)
        
        self._slider = canvas.create_rectangle(xPos, self._startYPos, xPos+width, self._startYPos+sliderHeight, fill=AppPalette.Yellow)
        canvas.tag_bind(self._slider, '<B1-Motion>',self.__motion) 
        #canvas.tag_bind(self._slider, '<Button-1>', self.btnDown)

    def OnUpdate(self, handler):
        self.__handlers.append(handler)
        return

    def setToValue(self, value):
        pos = self.__calcPositionFromValue(value)
        print(pos)
        self._updateSlider(pos)
        #self._updateSliderValue(value)

    def __motion(self, event):       
        self._updateSlider(event.y)
        self._updateSliderValue(event.y)
        return

    def _updateSlider(self, yPos):
        posDif = self.__getSliderMovementDifference(yPos)
        #draw slider
        self.__canvas.move(self._slider, 0, posDif)
        self.__canvas.update()
        return

    def _updateSliderValue(self, yPos):
        #get updated slider value
        val = self.__calcCurrentPosValue(yPos)
        #print (f"curent value is {val}")
        if val != self._lastVal:
            for handler in self.__handlers:
                handler(val)
        self._lastVal = val
        return

    def __calcCurrentPosValue(self, yPos):
        #get latest slider position
        curPosY1 = self.__canvas.coords(self._slider)[1] - self._objectYpos
        percent = 1 - (curPosY1 / self._sliderRange)
        return int((percent * (self._maxVal-self._minVal)) + self._minVal)

    def __calcPositionFromValue(self,value):
        percent = 1 - (value / (self._maxVal - self._minVal)) 
        return percent * self._sliderRange + (self._sliderHalfHeight + self.__yPos)


    def __getSliderMovementDifference(self, yPos):
        #get current slider position
        curPosY1 = self.__canvas.coords(self._slider)[1] - self._objectYpos
        curPosY2 = self.__canvas.coords(self._slider)[3] - self._objectYpos
        #get move value
        posDif = yPos - self.__canvas.coords(self._slider)[1]-self._sliderHalfHeight
        #disable overrun      
        if curPosY1+posDif < 0: posDif = 0 - curPosY1
        if curPosY2+posDif > self._height: posDif = self._height - curPosY2

        return posDif