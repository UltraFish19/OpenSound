#Meant to read and write data. 

import json

def ReadJson(Path : str) -> dict:
    with open(Path,"r") as File:
        return json.load(File)

def SaveJson(Path : str, Data : dict):
    with open(Path,"w") as File:
        json.dump(Data,File,indent=3)