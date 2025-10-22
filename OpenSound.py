# Opensound Main Module

import MusicService # Import the Music Service module
from TTSService import Say, SayThenLog # Text to speech service
import AppService # Host app
import datetime # Convert seconds to formatted time
from time import sleep

MusicService.InitAudio() # Initialize the audio system


AppService.HostApp()

sleep(1) # Skip the Flask yap fest




print("\n\n\n\n\n")

print("Welcome to OpenSound!") # Welcome message
print("Commands are: \n <URL> to play a song \n Pause to pause \n Play to resume \n Replay to play the cached song")







while True:
    UserInput = input("Enter a command or Song name: ") # Ask the user for a command or URL

    

    if UserInput.lower() == "pause": # If the user wants to pause the audio
        
        
        MusicService.SetAudioPlaying(False) # Pause the audio
        Say("Audio paused.")
        print("Audio paused.") # Inform the user that the audio is paused
    elif UserInput.lower() == "play": # If the user wants to resume the audio       
        MusicService.SetAudioPlaying(True) # Resume the audio
        Say("Audio unpaused.")
        print("Audio resumed.") # Inform the user that the audio is resumed
    elif UserInput.lower() == "replay":
        Say("Replaying song")
        MusicService.PlaySong(MusicService.CachePath + MusicService.ConvertedSongName,True)
    else: # Otherwise, assume the user entered a URL
        SearchResults = MusicService.SearchSong("Youtube Music" + UserInput)

        Say("Searching for " + UserInput)

        if len(SearchResults) == 0:
            SayThenLog("No search results for " + UserInput)
        else:
            print("Search results for " + UserInput)
            for Index, Result in enumerate(SearchResults):
                Index += 1

                try:
                    print(f"[{Index}]: {Result.title} by {Result.author}. Length: {str(datetime.timedelta(seconds=Result.length))}")
                except:
                    print(f"[{Index}]: SONG UNAVAILABLE")

            UserChoice = input("What song do you want to play. (Please put the number): ")

            SongToPlay = None # Keep it none for now

            try:
                SongToPlay = SearchResults[int(UserChoice) - 1]
            except ValueError:
                SayThenLog("Invalid input")
            except IndexError:
                SayThenLog("Invalid input, Number must be lower")

            if SongToPlay is not None:
                SayThenLog(f"Playing {SongToPlay.title}")
                MusicService.FetchSong(SongToPlay.watch_url)
            


            
                
                

        








# try:
#     SearchResults = MusicService.SearchSong(UserInput)

#     SearchResult = SearchResults[0] # First song on list

#     print(f"Playing {SearchResult.title}, by {SearchResult.author}.")

#     MusicService.FetchSong(SearchResult.watch_url) # Play video link
# except Exception as e:
#     print(f"Something went wrong, please try again. \n {e}")


