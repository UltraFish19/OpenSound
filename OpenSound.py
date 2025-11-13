# Opensound Main Module

import MusicService # Import the Music Service module
import DataService
from TTSService import Say, SayThenLog # Text to speech service
import AppService # Host app
from time import sleep
import json







MusicService.InitAudio(DataService.InternalSettings) # Initialize the audio system





AppService.HostApp()




