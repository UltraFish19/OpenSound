import datetime
from flask import Flask,render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
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

    MusicDetails["TimePosition"] = round((MusicService.pygame.mixer.music.get_pos()/ 1000))
    MusicDetails["Name"] = MusicService.CurrentlyPlaying
    MusicDetails["TimeLength"] = MusicService.CurrentSongLength 
    MusicDetails["IsPlaying"] = MusicService.CurrentSongPlaying

    ServerDetails = {}
    ServerDetails["Music"] = MusicDetails

    SendToClients(ServerDetails,SERVERDETAILS)








SearchDebounce = False # Add a debounce to prevent the function from running while it is currently searching
def SearchSongForClient(SearchQuery : str):
    global SearchDebounce

    try: 

        if SearchDebounce == False:

            SearchDebounce = True

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


            
            SearchDebounce = False
            


    except Exception as e: SearchDebounce = False; print(e) # Reset debounce after an error.



def PlaySoundForClient(Url):
    
    MusicService.FetchSong(Url,Announce=True)

def PauseSongForClient():
    MusicService.SetAudioPlaying(not MusicService.CurrentSongPlaying)
    


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
        Search = RequestData.get("Search")

        


        if Type == "SearchSongs":
            SearchSongForClient(Search)
        elif Type == "PlaySong":
            PlaySoundForClient(Search)
        elif Type == "PauseSong":
             # Toggle music pausingness
            PauseSongForClient()
        SendServerDetailsToClient()
        emit(GENERICRESPONSE,{"Status" : "Got Request"})

        
    def SendDataToClientLoop():
        while True:
            SendServerDetailsToClient()
            WebSocket.sleep(0.2)
        



    WebSocket.start_background_task(SendDataToClientLoop)

    WebSocket.run(App,host="0.0.0.0",port=5000)


    





def HostApp(): # NOT PRODUCTION
   threading.Thread(target=App,name="AppThread").start()

    