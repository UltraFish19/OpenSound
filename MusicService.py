# Opensound Music Service Module

from pytubefix import YouTube # Import YouTube from the module
import os # Import the OS module to handle file paths
import pydub # Audio libarary to handle audio files
from pydub.playback import play # Import the playback function from pydub
if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly





CachePath = R"C:\Users\rmohamma1884\OneDrive - Hamilton Wentworth District School Board\Documents\OpenSound\OpenSound\Cache\Music"
SongName = R"\Song.m4a"


pydub.AudioSegment.converter = R"C:\Users\rmohamma1884\Downloads\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg" # THIS WILL CHANGE ON LINUX 


def PlaySong(AudioPath): # This will play the song from the cache folder
    Audio = pydub.AudioSegment.from_file(AudioPath, codec="aac") # Load the audio file from the cache folder and play the AAC codec
    play(Audio) # Play the audio file


def FetchSong(Link): #This will download a the song from Youtube music, and play it.

    if os.path.exists(CachePath+SongName): # Check if the song already exists in the cache folder
        os.remove(CachePath+SongName) # Remove the old song from the cache folder if it exists

    YoutubeSong = YouTube(Link) # Get the Youtube link  
    Stream = YoutubeSong.streams.get_audio_only() # Get the audio only stream
    AudioDownload = Stream.download(output_path=CachePath) # Download the audio to the cache folder
    os.rename(AudioDownload, CachePath+SongName) # Rename the file to have a .mp4 extension, the variable will also be changed
    PlaySong(CachePath+SongName) # Play the song from the cache folder



