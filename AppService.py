from flask import Flask,render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import MusicService

if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly


    
def DoSmth(X):
    MusicService.PlaySimple(X)



def App(): 

    
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
            DoSmth(Search)
        elif Type == "PlaySong":
            pass

        

        emit("GenericReponse",{"Status" : "Got Request"})


    WebSocket.run(App,host="0.0.0.0",port=5000)


    





def HostApp(): # NOT PRODUCTION
   threading.Thread(target=App).start()

   
    