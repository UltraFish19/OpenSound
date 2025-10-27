import pyttsx3
import MusicService


if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly










def Say(Text : str): # Text to speech


    try:
        Engine = pyttsx3.init()
        MusicService.pygame.mixer.music.set_volume(50.0) # Set volume lower so people can actually hear the TTS
        Engine.say(Text)
        Engine.runAndWait()

        del Engine
        
        MusicService.pygame.mixer.music.set_volume(100.0)
    except:
        print("TTS already active")


def SayThenLog(Text : str): # Text to speech then also print it
    Say(Text)
    print(Text)


