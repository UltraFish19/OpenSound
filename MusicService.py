# Opensound Music Service Module


if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly

from io import FileIO
import os
from time import sleep

import DataService # Import the OS module to handle file paths
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pyglet
from pytubefix import YouTube # Import YouTube and Search from the module
from pytubefix.contrib.search import Search, Filter
import pydub # Audio libarary to handle audio files
from TTSService import Say









CachePath = ""
SongName = R"\Song.m4a" # .M4a name
ConvertedSongName = R"\Song.wav" # Name of song when converted to .WAV
MAXDURATION = 1200 # The maximum song length in seconds
NOSONGPLAYING = "" # The text that shows when no long is playing





AudioPlayer = pyglet.media.Player()
Clock = pyglet.clock
AudioSource : pyglet.media.StreamingSource = None
AudioFileHandle : FileIO = None



class SongInfo():
    Name = NOSONGPLAYING
    SongStreamEnabled = False # If the music is playing on Pyglet
    Duration = -10000 
    CurrentSongPlaying = False
    Author = "Unknown"
    IsFavourited = False
    CurrentUrl = ""

class SongTooLongError(Exception):
    def __init__(Self,Message=f"Your song is too long, the maximum length is {MAXDURATION} secs"):
        super().__init__(Message)

FAVSONGPATH = "Data\Favorites.json" # Where the file to store favourited songs is stored.

def CheckIfFavourited(Url):
    Data = DataService.ReadJson(FAVSONGPATH) # If url exists then it is favourited.
    if Data.get(Url):
        return True
    else:
        return False
    



def ToggleFavourite(Url,Name ="Unknown",Author = "Unknown"): # If faved it will remove otherwise it will add.
    Data = DataService.ReadJson(FAVSONGPATH)
    if CheckIfFavourited(Url) == False:
        Data[Url] = {
            "Name" : Name,
            "Author" : Author
        }
    else:
        Data.pop(Url)
        
    DataService.SaveJson(FAVSONGPATH,Data) # Finish by saving changes





def ConvertCodec(YoutubeAudioPath : str): # This will convert from .M4A to .WAV which works on Windows
    try:
        M4AAudio = pydub.AudioSegment.from_file(YoutubeAudioPath, codec="aac")
        M4AAudio.export(YoutubeAudioPath.replace(".m4a", ".wav"), format="wav") # Export the audio file as a .WAV file
        os.remove(YoutubeAudioPath) # Remove the old .M4A file
        return YoutubeAudioPath.replace(".m4a", ".wav") # Return the path of the new .WAV file
    except Exception as e: 
        print("Error converting audio file:", e) # Print an error message if the conversion fails
        return None # Return None if the conversion fails
    

def InitAudio(InternalData): # This will initialize the audio system
    global CachePath
    CachePath = InternalData["MusicCacheLocation"]
    pydub.AudioSegment.converter = InternalData["FFMpegConverterLocation"]
    




SongInfo.CurrentSongPlaying = False
def SetAudioPlaying(SetTo : bool):
    
    if SongInfo.SongStreamEnabled == True: # Prevent entire speaker from crashing
        if SetTo:
            AudioPlayer.play()
            SongInfo.CurrentSongPlaying = True
            Say("Resuming Audio")
        else:
            AudioPlayer.pause() # Pause the audio if SetTo is False
            SongInfo.CurrentSongPlaying = False
            Say("Pausing Audio")


def SetAudioDuration(SetTo : float):
    

    if SongInfo.SongStreamEnabled == True:
        Say(f"Setting duration")
        AudioPlayer.seek(SetTo)
        


def PlaySong(AudioPath, AlreadyConverted = False): # This will play the song from the cache folder
    global AudioSource,AudioPlayer, AudioFileHandle

    if AlreadyConverted == False:
        ConvertedPath = ConvertCodec(AudioPath) # Convert the audio file to .WAV

        if ConvertedPath is None: # Check if the conversion was successful
            print("Failed to convert audio file.") # Print an error message if the conversion failed
            return # Exit the function if the conversion failed
    else:
        ConvertedPath = AudioPath

  
    AudioPlayer = pyglet.media.Player() # Create player object.


    AudioFileHandle = open(ConvertedPath,"rb") 


    AudioSource = pyglet.media.load(ConvertedPath,file=AudioFileHandle,streaming=True) # Load the song from the cache folder

    SongInfo.Duration = AudioSource.duration

    AudioPlayer.queue(AudioSource)

    AudioPlayer.play() # Play the song

    SongInfo.CurrentSongPlaying = True
    SongInfo.SongStreamEnabled = True
    SongInfo.IsFavourited = CheckIfFavourited(SongInfo.CurrentUrl)
    

def SearchSong(SongName : str) :  # Music searching, Returns list of Youtube videos

    SongFilter = {
        "type" : Filter.get_type("Video"),
        "duration" : Filter.get_duration("4 - 20 minutes")
    }




    Results = Search(SongName, filters=SongFilter) # Search song with the given keywords


    return Results.videos


    
def UnloadAudio(): # Frees up old audio files and fully unloads.
    global AudioPlayer, AudioSource,AudioFileHandle

    if AudioFileHandle:
        AudioPlayer.delete()
        AudioSource.delete()
        AudioFileHandle.close()

    


def FetchSong(Link : str,Announce = False): #This will download a the song from Youtube music, and play it.

    global  AudioSource
    

    try:
        if os.path.exists(CachePath+SongName): # Check if the song already exists in the cache folder
            os.remove(CachePath+SongName) # Remove the old song from the cache folder if it exists

        if os.path.exists(CachePath+ConvertedSongName): # Check if the converted song already exists in the cache folder
            SongInfo.SongStreamEnabled = False


            
            

            UnloadAudio()    
            os.remove(CachePath+ConvertedSongName) # Remove the converted song if it exists

        YoutubeSong = YouTube(Link) # Get the Youtube link  


        Length = YoutubeSong.length

        


        if Length > MAXDURATION: # Prevent anyone from downloading a 24 hour long video.
            raise SongTooLongError
        

        # Anything dealing with playback and song information should be below this.

        Title = YoutubeSong.title
        Author = YoutubeSong.author

        SongInfo.Author = Author
        SongInfo.CurrentUrl = Link

        SongInfo.Name = Title
        SongInfo.IsFavourited = CheckIfFavourited(SongInfo.CurrentUrl)

        Stream = YoutubeSong.streams.get_audio_only() # Get the audio only stream
        Stream.download(output_path=CachePath,filename=SongName) # Download the audio to the cache folder and rename it
        
 
        SongInfo.Duration = -10000 # Force bar to the left.

        if Announce == True:
            Say(f"Playing {Title} by {Author}" )

        PlaySong(CachePath+SongName) # Play the song from the cache folder
    except Exception as e:
        print(f"Failed to download song. \n {e}")
        if Announce == True:
            Say("Failed to download song!")




def PlaySimple(Search):
    try:

        Say("Searching for" + Search)
        SearchResults = SearchSong(Search)

        SearchResult = SearchResults[0] # First song on list

        Say(f"Playing {SearchResult.title}, by {SearchResult.author}.")

        FetchSong(SearchResult.watch_url) # Play video link
    except Exception as e:
        Say(f"Something went wrong, please try again. \n {e}")

