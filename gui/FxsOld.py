import copy

class Fxs:
    def __init__(self, fxData, fxParamsData, midiMaster):
        self.__midiUpdateHandlers = []
        self.__fxUpdateHandlers = []
        self.currentInstrument = ""#{}#firstFx
        self.__fxParamsData = fxParamsData
        self.fxData = self.__filterFxData(fxData,fxParamsData)
        self.__midiMaster = midiMaster
        #self.__midiMaster.onUpdate(self.midiInHandler)
        self.__curFxSettings = {}
        #self.__loadCurrentSettingsForAll()
        
    def onMidiInUpdate(self, handler):
        self.__midiUpdateHandlers.append(handler)

    def onInstrumentUpdate(self, handler):
        self.__fxUpdateHandlers.append(handler)

    def getFxList(self):
        return list(self.fxData.keys())

    def getCurentSettings(self):
        #print(self.__curFxSettings)
        return self.__curFxSettings.items()

    def setFx(self, fxName):
        self.currentInstrument = fxName
        #index = self.getFxList().index(self.currentInstrument)
        #self.__midiMaster.midiOut.sendProgramChange(index)
        self.__loadCurrentSettings()
        for handler in self.__fxUpdateHandlers:
            handler(fxName)

    def setFxSetting(self, settingName, value):
        self.__curFxSettings[settingName] = float(value)
        #self.__midiMaster.sendControlOutputForControlName(settingName, self.__scaleTo0To100ForControlName(value, settingName))
    
    def getControlRangeData(self, controlName):
        data = self.__fxParamsData[controlName]
        start = float(data["start_value"])
        stop = float(data["stop_value"])
        return [start, stop]

    def __filterFxData(self, fxData, paramData):
        filteredDict = {}
        namesToUse = ({k:v for (k,v) in paramData.items() if v["type"] == "range"}).keys()
        for instName,controlData in fxData.items():
            filteredData = {k: controlData[k] for k in namesToUse if k in controlData.keys() }
            filteredDict[instName] = filteredData

        return filteredDict

    def __loadCurrentSettings(self):
        self.__curFxSettings = self.fxData[self.currentInstrument]
        print(self.__curFxSettings.items())
        for key, value in self.__curFxSettings.items():
            self.setFxSetting(key,value)

    # def __scaleTo0To100ForControlName(self, val, name):
    #     low = float(self.__fxParamsData[name]["start_value"])
    #     high = float(self.__fxParamsData[name]["stop_value"])
    #     value = float(val)
    #     if value < low:
    #         value = low
    #         print(f"{val} below low range of {low}")
    #     elif value > high:
    #         value = high
    #         print(f"{val} above high range of {high}")
    #     return ((value-low) / (high - low)) * 100

    # def __scaleToExpectedRangeFrom0To100(self, val, name):
    #     low = float(self.__fxParamsData[name]["start_value"])
    #     high = float(self.__fxParamsData[name]["stop_value"])
    #     value = float(val)
        
    #     return (((high - low) / 100)*value) + low

    # def midiInHandler(self, controlName, value):
    #     self.__curFxSettings[controlName] = self.__scaleToExpectedRangeFrom0To100(value, controlName)
    #     print(self.__curFxSettings[controlName])
    #     for handler in self.__midiUpdateHandlers:
    #         handler(controlName, self.__curFxSettings[controlName])