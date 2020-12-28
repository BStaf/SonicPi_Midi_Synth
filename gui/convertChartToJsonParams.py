import os
import json 

readFilePath = os.path.dirname(os.path.realpath(__file__)) +"/notes/parameters.txt"
outFilePath = os.path.dirname(os.path.realpath(__file__)) +"/InstrumentParameters.Json"
headers = []
dataDict = {}

with open(readFilePath, 'r') as reader:
    for line in reader.readlines(): 
        if not headers:
            for item in line.strip('\n').split("\t")[1:]:
                headers.append(item)    
        else:
            inst = "x"
            temp = {}
            i = 0
            items = line.strip('\n').split("\t")
            while i < len(items):
                if (i == 0):#Instrument Name
                    inst = items[i]
                else:
                    if items[i]:
                        temp[headers[i-1]] = items[i]
                i = i+1
            dataDict[inst] = temp

jsonOut = json.dumps(dataDict, indent = 4)  
with open(outFilePath, 'w') as writer:
    writer.write(jsonOut)
print(jsonOut)
print(headers)