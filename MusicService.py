# Opensound Music Service Module

import pygame
from pytubefix import YouTube # Import YouTube from the module
import os # Import the OS module to handle file paths
import pydub # Audio libarary to handle audio files
from pydub.playback import play # Import the playback function from pydub
from pydub import AudioSegment
if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly


CachePath = R"C:\Users\rmohamma1884\OneDrive - Hamilton Wentworth District School Board\Documents\OpenSound\OpenSound\Cache\Music"
SongName = R"\Song.m4a" # .M4a name
ConvertedSongName = R"\Song.wav" # Name of song when converted to .WAV


pydub.AudioSegment.converter = R"C:\Users\rmohamma1884\Downloads\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg" # THIS WILL CHANGE ON LINUX 


def ConvertCodec(YoutubeAudioPath): # This will convert from .M4A to .WAV which works on Pygame
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


def PlaySong(AudioPath): # This will play the song from the cache folder

    ConvertedPath = ConvertCodec(AudioPath) # Convert the audio file to .WAV

    if ConvertedPath is None: # Check if the conversion was successful
        print("Failed to convert audio file.") # Print an error message if the conversion failed
        return # Exit the function if the conversion failed

    pygame.mixer.music.load(ConvertedPath) # Load the song from the cache folder
    pygame.mixer.music.play() # Play the song
    




def FetchSong(Link): #This will download a the song from Youtube music, and play it.

    if os.path.exists(CachePath+SongName): # Check if the song already exists in the cache folder
        os.remove(CachePath+SongName) # Remove the old song from the cache folder if it exists

    if os.path.exists(CachePath+ConvertedSongName): # Check if the converted song already exists in the cache folder
        pygame.mixer.music.unload() # Unload the previous song if there was one
        os.remove(CachePath+ConvertedSongName) # Remove the converted song if it exists

    YoutubeSong = YouTube(Link) # Get the Youtube link  
    Stream = YoutubeSong.streams.get_audio_only() # Get the audio only stream
    AudioDownload = Stream.download(output_path=CachePath) # Download the audio to the cache folder
    os.rename(AudioDownload, CachePath+SongName) # Rename the file to have a .mp4 extension, the variable will also be changed
    PlaySong(CachePath+SongName) # Play the song from the cache folder