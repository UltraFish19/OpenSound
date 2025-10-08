# Opensound Main Module

import MusicService # Import the Music Service module


MusicService.InitAudio() # Initialize the audio system


print("Welcome to OpenSound!") # Welcome message
print("Commands are: \n <URL> to play a song \n Pause to pause \n Play to resume")


while True:
    UserInput = input("Enter a command or URL: ") # Ask the user for a command or URL

    if UserInput.lower() == "pause": # If the user wants to pause the audio
        MusicService.SetAudioPlaying(False) # Pause the audio
        print("Audio paused.") # Inform the user that the audio is paused
    elif UserInput.lower() == "play": # If the user wants to resume the audio
        MusicService.SetAudioPlaying(True) # Resume the audio
        print("Audio resumed.") # Inform the user that the audio is resumed
    else: # Otherwise, assume the user entered a URL
        MusicService.FetchSong(UserInput) # Ask the user for a link, and play the song

