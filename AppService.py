from flask import Flask,render_template, request, jsonify
import threading
import TTSService

if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly


    
def DoSmth(X):
    TTSService.Say(X)



def App(): 

    
    App = Flask(__name__)





    @App.route("/",methods=["POST","GET"]) # Home page
    def HomePage():
        return render_template("HomeScreen.html")

    @App.route("/Music")
    def MusicPlayer():
        return render_template("Music.html")
    


    @App.route("/SendForm",methods=["POST"])
    def ReceiveData():
        DataFromSite : dict = request.get_json()

        if not DataFromSite:
            return jsonify({"error": "Invalid JSON"}), 400 # Return an error when something goes wrong
        
        Type = DataFromSite.get("RequestType")
        Search = DataFromSite.get("Search")

        if Type == "SearchSongs":
            DoSmth(Search)
        elif Type == "PlaySong":
            pass

        return "{Data : 'Got Data'}"


    App.run(host="0.0.0.0",port=5000)


    





def HostApp(): # NOT PRODUCTION
   threading.Thread(target=App).start()

   
    