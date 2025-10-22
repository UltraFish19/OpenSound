from flask import Flask, request
import threading


if __name__ == "__main__": # This will prevent the file from being run directly
    print("This is a module, and should not be run directly.") # Warn the user if they try to run this file directly
    exit() # Exit if this file is run directly



def App(): 

    
    App = Flask(__name__)





    @App.route("/")
    def HomePage():
        return "<p>Hello, World!</p>"

    App.run()


    





def HostApp(): # NOT PRODUCTION
   AppThread = threading.Thread(target=App).start()

   
    