from flask import Flask,render_template
import threading


if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly



def App(): 

    
    App = Flask(__name__)





    @App.route("/",methods=["POST","GET"]) # Home page
    def HomePage():
        return render_template("HomeScreen.html")

    @App.route("/Music")
    def MusicPlayer():
        return render_template("Music.html")


    App.run()


    





def HostApp(): # NOT PRODUCTION
   threading.Thread(target=App).start()

   
    