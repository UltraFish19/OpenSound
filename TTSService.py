import pyttsx3

Engine = pyttsx3.init()





def Say(Text : str): # Text to speech
    pyttsx3.speak(Text)



def SayThenLog(Text : str): # Text to speech then also print it
    Say(Text)
    print(Text)


