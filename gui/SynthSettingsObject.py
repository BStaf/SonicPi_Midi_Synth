from abc import ABC, abstractmethod

class SynthSettingsObject(ABC):
    def __init__(self, synthOjectData, synthParamsData, midiMaster):
        self._midiUpdateHandlers = []
        self._currentObject = {}
        self._objectParamsData = synthParamsData
        self._objectData = self.__filterObjectData(synthOjectData, synthParamsData)
        self._midiMaster = midiMaster
        
    def onMidiInUpdate(self, handler):
        self._midiUpdateHandlers.append(handler)

    def getList(self):
        return list(self._objectData.keys())

    def getCurentSettings(self):
        return self._currentObject.items()

    @abstractmethod
    def setCurrent(self, name):
        self._currentObject = self._objectData[name]

    @abstractmethod
    def setSetting(self, name, value):
        self._currentObject[name] = float(value)
        scaledVal = self._scaleTo0To100ForControlName(value, name)
        self._midiMaster.sendControlOutputForControlName(name, scaledVal)
    
    def getControlRangeData(self, name):
        data = self._objectParamsData[name]
        start = float(data["start_value"])
        stop = float(data["stop_value"])
        return [start, stop]

    def __filterObjectData(self, objectData, paramData):
        filteredDict = {}
        namesToUse = ({k:v for (k,v) in paramData.items() if v["type"] == "range"}).keys()
        for name,controlData in objectData.items():
            filteredData = {k: controlData[k] for k in namesToUse if k in controlData.keys() }
            filteredDict[name] = filteredData

        return filteredDict

    def _scaleTo0To100ForControlName(self, val, name):
        low = float(self._objectParamsData[name]["start_value"])
        high = float(self._objectParamsData[name]["stop_value"])
        value = float(val)
        if value < low:
            value = low
            print(f"{val} below low range of {low}")
        elif value > high:
            value = high
            print(f"{val} above high range of {high}")
        return ((value-low) / (high - low)) * 100

    def _scaleToExpectedRangeFrom0To100(self, val, name):
        #print(self._objectParamsData)
        #print(f"{name}-{val}")
        low = float(self._objectParamsData[name]["start_value"])
        high = float(self._objectParamsData[name]["stop_value"])
        value = float(val)
        
        return (((high - low) / 100)*value) + low
