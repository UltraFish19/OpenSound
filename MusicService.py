# Opensound Music Service Module

import pygame
from pytubefix import YouTube # Import YouTube and Search from the module
from pytubefix.contrib.search import Search, Filter
import os # Import the OS module to handle file paths
import pydub # Audio libarary to handle audio files
from pydub.playback import play # Import the playback function from pydub
from pydub import AudioSegment
from TTSService import Say


if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly






CachePath = R"C:\Users\rmohamma1884\OneDrive - Hamilton Wentworth District School Board\Documents\OpenSound\OpenSound\Cache\Music"
SongName = R"\Song.m4a" # .M4a name
ConvertedSongName = R"\Song.wav" # Name of song when converted to .WAV
MAXLENGTH = 600 # The maximum song length in seconds

pydub.AudioSegment.converter = R"C:\Users\rmohamma1884\Downloads\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg" # THIS WILL CHANGE ON LINUX 


class SongTooLongError(Exception):
    def __init__(Self,Message=f"Your song is too long, the maximum length is {MAXLENGTH} secs"):
        super().__init__(Message)



def ConvertCodec(YoutubeAudioPath : str): # This will convert from .M4A to .WAV which works on Pygame
    try:
        M4AAudio = pydub.AudioSegment.from_file(YoutubeAudioPath, codec="aac")
        M4AAudio.export(YoutubeAudioPath.replace(".m4a", ".wav"), format="wav") # Export the audio file as a .WAV file
        os.remove(YoutubeAudioPath) # Remove the old .M4A file
        return YoutubeAudioPath.replace(".m4a", ".wav") # Return the path of the new .WAV file
    except Exception as e: 
        print("Error converting audio file:", e) # Print an error message if the conversion fails
        return None # Return None if the conversion fails
    

def InitAudio(): # This will initialize the audio system
    pygame.mixer.init() # Initialize the mixer module in Pygame

def SetAudioPlaying(SetTo : bool):
    if SetTo:
        pygame.mixer.music.unpause() # Resume the audio if SetTo is True
    else:
        pygame.mixer.music.pause() # Pause the audio if SetTo is False


def PlaySong(AudioPath, AlreadyConverted = False): # This will play the song from the cache folder


    if AlreadyConverted == False:
        ConvertedPath = ConvertCodec(AudioPath) # Convert the audio file to .WAV

        if ConvertedPath is None: # Check if the conversion was successful
            print("Failed to convert audio file.") # Print an error message if the conversion failed
            return # Exit the function if the conversion failed
    else:
        ConvertedPath = AudioPath

    pygame.mixer.music.load(ConvertedPath) # Load the song from the cache folder
    pygame.mixer.music.play() # Play the song
    

def SearchSong(SongName : str) :  # Music searching, Returns list of Youtube videos

    SongFilter = {
        "type" : Filter.get_type("Video"),
        "duration" : Filter.get_duration("4 - 20 minutes")
    }




    Results = Search(SongName, filters=SongFilter) # Search song with the given keywords


    return Results.videos


    
    


def FetchSong(Link : str): #This will download a the song from Youtube music, and play it.

    try:
        if os.path.exists(CachePath+SongName): # Check if the song already exists in the cache folder
            os.remove(CachePath+SongName) # Remove the old song from the cache folder if it exists

        if os.path.exists(CachePath+ConvertedSongName): # Check if the converted song already exists in the cache folder
            pygame.mixer.music.unload() # Unload the previous song if there was one
            os.remove(CachePath+ConvertedSongName) # Remove the converted song if it exists

        YoutubeSong = YouTube(Link) # Get the Youtube link  

        if YoutubeSong.length > MAXLENGTH: # Prevent anyone from downloading a 24 hour long video.
            raise SongTooLongError

        Stream = YoutubeSong.streams.get_audio_only() # Get the audio only stream
        AudioDownload = Stream.download(output_path=CachePath) # Download the audio to the cache folder
        os.rename(AudioDownload, CachePath+SongName) # Rename the file to have a .mp4 extension, the variable will also be changed
        PlaySong(CachePath+SongName) # Play the song from the cache folder
    except Exception as e:
        print(f"Failed to download song. \n {e}")




def PlaySimple(Search):
    try:

        Say("Searching for" + Search)
        SearchResults = SearchSong(Search)

        SearchResult = SearchResults[0] # First song on list

        Say(f"Playing {SearchResult.title}, by {SearchResult.author}.")

        FetchSong(SearchResult.watch_url) # Play video link
    except Exception as e:
        Say(f"Something went wrong, please try again. \n {e}")


