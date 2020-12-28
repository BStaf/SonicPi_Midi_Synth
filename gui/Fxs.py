from SynthSettingsObject import *
import copy

class Fxs(SynthSettingsObject):
    def __init__(self, fxData, fxParamsData, midiMaster):
        SynthSettingsObject.__init__(self, fxData, fxParamsData, midiMaster)
        self._midiMaster.onUpdate(self.midiInHandler)
        self.__updatgeAllFxSettings()

    def setCurrent(self, name):
        #self.currentInstrument = name
        index = super().getList().index(name)
        #self._midiMaster.midiOut.sendProgramChange(index)

        super().setCurrent(name)

    def setSetting(self, name, value):
        super().setSetting(name,value)
      #  val = value / 100.0
        #self.__curInstSettings[settingName] = float(value)
        #self.__midiMaster.sendControlOutputForControlName(settingName, self.__scaleTo0To100ForControlName(value, settingName))
    
    def midiInHandler(self, name, value):
        print(f"midi In {name}")
        self._currentObject[name] = self._scaleToExpectedRangeFrom0To100(value, name)
        #print(self.__curInstSettings[controlName])
        for handler in self._midiUpdateHandlers:
            handler(name, self._currentObject[name])

    def __updatgeAllFxSettings(self):
        #send midicommands to set all fx to base values
        #print(self._objectData)
        for fxObject in self._objectData.values():
            for name, value in fxObject.items():
                #print(f"{name}-{value}")
                scaledVal = self._scaleTo0To100ForControlName(value, name)
                self._midiMaster.sendControlOutputForControlName(name, scaledVal)
            #filteredData = {k: controlData[k] for k in namesToUse if k in controlData.keys() }
            #filteredDict[name] = filteredData
