import os
import json 

controlDataPath = os.path.dirname(os.path.realpath(__file__)) +"/ControlData.Json"
paramsPath = os.path.dirname(os.path.realpath(__file__)) +"/ControlParameters.Json"

def makeName(name):
    varName = '_'.join([(i[0].upper() + i[1:]) for i in name.split("_")]) 
    return f"ENV_{varName}"

with open(paramsPath, 'r') as reader:
    paramData = json.load(reader)

with open(controlDataPath, 'r') as reader:
    controlData = json.load(reader)

for key, value in paramData.items():
    if value["type"] == "range":
        midiOut = controlData[key]["midi_out_control"]
        startVal = value["start_value"]
        stopVal = value["stop_value"]
        varName = makeName(key)
        print(f"elsif cntrlNum == {midiOut}")
        print(f"\t{varName} = scaleMidiAi cntrlValue, {startVal}, {stopVal}")



