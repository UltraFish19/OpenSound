#Meant to read and write data. 


if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly

import json


InternalSettings = json.load(open(R"Data\InternalSettings.json","r"))


def ReadJson(Path : str) -> dict:
    with open(Path,"r") as File:
        return json.load(File)

def SaveJson(Path : str, Data : dict):
    with open(Path,"w") as File:
        json.dump(Data,File,indent=3)

def GetCorrectPath():
    pass