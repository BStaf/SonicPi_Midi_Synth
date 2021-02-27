import os
import json 

midiControlDataPath = os.path.dirname(os.path.realpath(__file__)) +"/config/ControlData.Json"
paramsPath = os.path.dirname(os.path.realpath(__file__)) +"/config/instrumentParameters.Json"
controlDataPath = os.path.dirname(os.path.realpath(__file__)) +"/config/InstrumentData.Json"

def makeName(name):
    varName = '_'.join([(i[0].upper() + i[1:]) for i in name.split("_")]) 
    return f"{varName}"


with open(paramsPath, 'r') as reader:
    paramData = json.load(reader)

with open(midiControlDataPath, 'r') as reader:
    midiControlData = json.load(reader)

with open(controlDataPath, 'r') as reader:
    controlData = json.load(reader)

for key, value in paramData.items():
    if value["type"] == "range":
        midiOut = midiControlData[key]["midi_out_control"]
        #print(f"keys:  {key}")
        #print(controlData[getDataKey(key)])
        #initialVal = controlData[key][key]
        startVal = value["start_value"]
        stopVal = value["stop_value"]
        varName = makeName(key)
        #print(initialVal)
        print("{:"+varName+ " => {:control => "+midiOut+", :val => , :min => "+startVal+", :max => "+stopVal+" },")
        #print(f"elsif cntrlNum == {midiOut}")
        #print(f"\t{varName} = scaleMidiAi cntrlValue, {startVal}, {stopVal}")



