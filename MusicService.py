# Opensound Music Service Module

import pytubefix # Install the main module for it
from pytubefix import YouTube # Import YouTube from the module
import os # Import the OS module to handle file paths
from playsound import playsound as Playsound # Import the playsound module to play audio

if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly





CachePath = R"C:\Users\rmohamma1884\OneDrive - Hamilton Wentworth District School Board\Documents\OpenSound\OpenSound\Cache\Music"
SongName = R"\Song.m4a"




def PlaySong(Link): #This will download a the song from Youtube music, and play it.

    if os.path.exists(CachePath+SongName): # Check if the song already exists in the cache folder
        os.remove(CachePath+SongName) # Remove the old song from the cache folder if it exists

    YoutubeSong = YouTube(Link) # Get the Youtube link  
    Stream = YoutubeSong.streams.get_audio_only() # Get the audio only stream
    AudioDownload = Stream.download(output_path=CachePath) # Download the audio to the cache folder
    os.rename(AudioDownload, CachePath+SongName) # Rename the file to have a .mp4 extension, the variable will also be changed
    Playsound(CachePath+SongName) # Play the song from the cache folder



