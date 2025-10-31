# Opensound Main Module

import MusicService # Import the Music Service module
from TTSService import Say, SayThenLog # Text to speech service
import AppService # Host app
import datetime # Convert seconds to formatted time
from time import sleep

MusicService.InitAudio() # Initialize the audio system


AppService.HostApp()




