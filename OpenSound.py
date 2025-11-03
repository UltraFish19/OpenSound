# Opensound Main Module

import MusicService # Import the Music Service module
from TTSService import Say, SayThenLog # Text to speech service
import AppService # Host app
from time import sleep
import json



InternalData = json.load(open(R"Data\InternalSettings.json","r"))



MusicService.InitAudio(InternalData) # Initialize the audio system





AppService.HostApp()




