import datetime
from flask import Flask,render_template
from flask_socketio import SocketIO, emit
import threading
import DataService
import MusicService
from TTSService import Say, SayThenLog

if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly

WebSocket : SocketIO



# Create Constants for common strings
GENERICRESPONSE = "GenericResponse" # Send whenever client sends data.
SERVERDETAILS = "ServerDetails" # Will contain system information.
SEARCHRESULTS = "SearchResults" # Send search results.


    
#Do certain actions outside the App thread to prevent any silly issues and race conditions.



def SendToClients(Data : dict, Type): # Should only be accessed from outside the App thread
    # Each Type should be in its correct format. (eg. SEARCHRESULTS should be in the proper dictionary format) 
    global WebSocket
    WebSocket.emit(Type,Data) # Send to everyone connected.




def SendServerDetailsToClient():
    MusicDetails = {} # Store details here

    MusicDetails["TimePosition"] = MusicService.AudioPlayer.time
    MusicDetails["Name"] = MusicService.SongInfo.Name
    MusicDetails["TimeLength"] = MusicService.SongInfo.Duration
    MusicDetails["IsPlaying"] = MusicService.SongInfo.CurrentSongPlaying
    MusicDetails["IsFavourited"] = MusicService.SongInfo.IsFavourited # If song is favourited or not. This is purely for the button.
    MusicDetails["CurrentUrl"] = MusicService.SongInfo.CurrentUrl
    MusicDetails["SongLoaded"] = MusicService.SongInfo.SongStreamEnabled
    MusicDetails["IsLooping"] = MusicService.SongInfo.IsLooping # Also for the button appearance.
    ServerDetails = {}
    ServerDetails["Music"] = MusicDetails

    SendToClients(ServerDetails,SERVERDETAILS)








SearchDebounce = False # Add a debounce to prevent the function from running while it is currently searching
def SearchSongForClient(SearchQuery : str,ShowFavourites = False):
    global SearchDebounce

    if SearchQuery.startswith(MusicService.DIRECTPLAYPREFIX): # Directly play from URL
        PlaySoundForClient(SearchQuery) # In this case the Query is the song Url
        return

    try: 

        if SearchDebounce == False:

            SearchDebounce = True
            if ShowFavourites == False:
                Say(f"Searching for {SearchQuery}")


                SearchResults = MusicService.SearchSong(SearchQuery)



                for I,Result in enumerate(SearchResults,start=1):

                    
                    ResultDict = {} # Hold onto data for a specific search result

                    try: # Omit the result if it is unavilable
                        Result.check_availability()
                    except:
                        continue

                    DataToSend = {}

                    # Look at "Misc\SearchResultsTemplate.json" to see how the data format is going to be like.
                    ResultDict["Name"] = Result.title
                    ResultDict["Duration"] = str(datetime.timedelta(seconds=Result.length))
                    ResultDict["Author"] = Result.author
                    ResultDict["Url"] = Result.watch_url

                    DataToSend["Result"] = ResultDict

                    AdditionalDataDict = {}
                    AdditionalDataDict["Query"] = SearchQuery
                    AdditionalDataDict["ResultsSent"] = I

                    if I == 1: # Let all clients know to remove old searchs
                        AdditionalDataDict["RemovePreviousResults"] = True
                    else:
                        AdditionalDataDict["RemovePreviousResults"] = False
                    
                    DataToSend["Details"] = AdditionalDataDict

                    SendToClients(DataToSend,SEARCHRESULTS)
            else:
                Say("Showing Favorites")
                Data = DataService.ReadJson(MusicService.FAVSONGPATH)
                
                
                for I,SongUrl in enumerate(Data.keys(), start=1):
                    DataToSend = {}
                    ResultDict = {}
                    SongData = Data[SongUrl]
                    ResultDict["Name"] = SongData["Name"]
                    ResultDict["Duration"] = "WIP"
                    ResultDict["Author"] = SongData["Author"]
                    ResultDict["Url"] = SongUrl

                    AdditionalDataDict = {}
                    AdditionalDataDict["Query"] = "Favourited Song"
                    AdditionalDataDict["ResultsSent"] = I

                    if I == 1: # Let all clients know to remove old searchs
                        AdditionalDataDict["RemovePreviousResults"] = True
                    else:
                        AdditionalDataDict["RemovePreviousResults"] = False

                    DataToSend["Details"] = AdditionalDataDict
                    DataToSend["Result"] = ResultDict
                    SendToClients(DataToSend,SEARCHRESULTS)

            
            SearchDebounce = False
            


    except Exception as e: SearchDebounce = False; print(e) # Reset debounce after an error.



def PlaySoundForClient(Url):
    
    MusicService.FetchSong(Url,Announce=True)

def PauseSongForClient():
    MusicService.SetAudioPlaying(not MusicService.SongInfo.CurrentSongPlaying)
    
def SetSongDurationForClient(To):
    MusicService.SetAudioDuration(float(To))

def ToggleLoopForClient(): # Make song looped or not
    MusicService.SongInfo.IsLooping = not MusicService.SongInfo.IsLooping # Inverse the boolean
    if MusicService.AudioPlayer:
        MusicService.AudioPlayer.loop = MusicService.SongInfo.IsLooping

def App(): 

    global WebSocket

    App = Flask(__name__)
    WebSocket = SocketIO(App) # Create the websocket for fast bidirectional communication




    @App.route("/",methods=["POST","GET"]) # Home page
    def HomePage():
        return render_template("HomeScreen.html")

    @App.route("/Music")
    def MusicPlayer():
        return render_template("Music.html")
    



    @WebSocket.on("connect") # By default this will run whenever something connect.
    def HandleClientConnection():
        print("Client connection detected")
        emit("GenericResponse",{"Status" : "Hello from the server, and welcome to OpenSound"})
   

    @WebSocket.on("ClientSubmit") # This will handle whenever a Client wants to do something to the Server
    def HandleClientSubmit(RequestData): # Gives a JSON for whatever the client needs
        print(RequestData)

        Type = RequestData.get("RequestType")
        Data = RequestData.get("Data")

        


        if Type == "SearchSongs": # Search for songs
            SearchSongForClient(Data)
        elif Type == "PlaySong": # Play a song via url
            PlaySoundForClient(Data)
        elif Type == "PauseSong": # Toggle music pausingness
             
            PauseSongForClient()
        elif Type == "SetDuration": # Set currently playing duration
            SetSongDurationForClient(Data)
        elif Type == "SetFavourite": # Set song to be favourited
            if MusicService.SongInfo.SongStreamEnabled == True:
                MusicService.ToggleFavourite(Data,MusicService.SongInfo.Name,MusicService.SongInfo.Author)
                

                if Data == MusicService.SongInfo.CurrentUrl and Data != "": # Prevent favouriting while invalid data.

                    MusicService.SongInfo.IsFavourited = not MusicService.SongInfo.IsFavourited
        elif Type == "ShowFavourites": # Show songs that are favourited
            SearchSongForClient("",True)
        elif Type == "ToggleLoop":
            ToggleLoopForClient()

        SendServerDetailsToClient()
        emit(GENERICRESPONSE,{"Status" : "Got Request"})

        
    def SendDataToClientLoop():
        while True:
            SendServerDetailsToClient()
            MusicService.Clock.tick() # Tick Pyglet clock
            MusicService.pyglet.app.platform_event_loop.dispatch_posted_events() # Update events
            WebSocket.sleep(0.2)
        



    WebSocket.start_background_task(SendDataToClientLoop)

    WebSocket.run(App,host="0.0.0.0",port=5000,allow_unsafe_werkzeug=True)


    





def HostApp(): # NOT PRODUCTION
   threading.Thread(target=App,name="AppThread").start()

    