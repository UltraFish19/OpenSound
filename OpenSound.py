# Opensound Main Module

import MusicService # Import the Music Service module


MusicService.InitAudio() # Initialize the audio system


print("Welcome to OpenSound!") # Welcome message
print("Commands are: \n <URL> to play a song \n Pause to pause \n Play to resume \n Replay to play the cached song")







while True:
    UserInput = input("Enter a command or Song name: ") # Ask the user for a command or URL

    if UserInput.lower() == "pause": # If the user wants to pause the audio
        MusicService.SetAudioPlaying(False) # Pause the audio
        print("Audio paused.") # Inform the user that the audio is paused
    elif UserInput.lower() == "play": # If the user wants to resume the audio
        MusicService.SetAudioPlaying(True) # Resume the audio
        print("Audio resumed.") # Inform the user that the audio is resumed
    elif UserInput.lower() == "replay":
        MusicService.PlaySong(MusicService.CachePath + MusicService.ConvertedSongName,True)
    else: # Otherwise, assume the user entered a URL
        

        try:
            SearchResults = MusicService.SearchSong(UserInput)

            SearchResult = SearchResults[0] # First song on list

            print(f"Playing {SearchResult.title}, by {SearchResult.author}.")

            MusicService.FetchSong(SearchResult.watch_url) # Play video link
        except Exception as e:
            print(f"Something went wrong, please try again. \n {e}")


