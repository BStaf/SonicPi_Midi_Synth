import os
import json 

midiControlDataPath = os.path.dirname(os.path.realpath(__file__)) +"/config/ControlData.Json"
paramsPath = os.path.dirname(os.path.realpath(__file__)) +"/config/FxParameters.Json"
controlDataPath = os.path.dirname(os.path.realpath(__file__)) +"/config/FxData.Json"

def makeName(name):
    varName = '_'.join([(i[0].upper() + i[1:]) for i in name.split("_")]) 
    return f"{varName}"

def getDataKey(name):
    return name.split("_")[0]

with open(paramsPath, 'r') as reader:
    paramData = json.load(reader)

with open(midiControlDataPath, 'r') as reader:
    midiControlData = json.load(reader)

with open(controlDataPath, 'r') as reader:
    controlData = json.load(reader)

for key, value in paramData.items():
    if value["type"] == "range":
        midiOut = midiControlData[key]["midi_out_control"]
        #print(f"keys: {getDataKey(key)} - {key}")
        #print(controlData[getDataKey(key)])
        initialVal = controlData[getDataKey(key)][key]
        startVal = value["start_value"]
        stopVal = value["stop_value"]
        varName = makeName(key)
        #print(initialVal)
        print("{:"+varName+ " => {:control => "+midiOut+", :val => "+initialVal+", :min => "+startVal+", :max => "+stopVal+" },")
        #print(f"elsif cntrlNum == {midiOut}")
        #print(f"\t{varName} = scaleMidiAi cntrlValue, {startVal}, {stopVal}")



