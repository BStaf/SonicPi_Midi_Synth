from .SynthSettingsObject import *
import copy

class Instruments(SynthSettingsObject):
    def __init__(self, instrumentData, instrumentParamsData, firstInstrument, midiMaster):
        SynthSettingsObject.__init__(self, instrumentData, instrumentParamsData, midiMaster)
        self._midiMaster.onUpdate(self.midiInHandler)
        self.setCurrent(firstInstrument)

    def setCurrent(self, name):      
        super().setCurrent(name)
        self.currentInstrument = name
        index = super().getList().index(name)
        for key, value in self._currentObject.items():
            self.setSetting(key,value)
        self._midiMaster.midiOut.sendProgramChange(index)      

    def setSetting(self, name, value):
        super().setSetting(name,value)

    def midiInHandler(self, name, value):
        print(f"midi In {name}")
        self._currentObject[name] = self._scaleToExpectedRangeFrom0To100(value, name)
        #print(self.__curInstSettings[controlName])
        for handler in self._midiUpdateHandlers:
            handler(name, self._currentObject[name])
