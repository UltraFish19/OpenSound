# Opensound Main Module

import MusicService # Import the Music Service module 
import DataService
import AppService # Host app
from time import sleep
from TTSService import Say, FormatIP

MusicService.InitAudio(DataService.InternalSettings) # Initialize the audio system


AppService.HostApp()

IP = FormatIP(AppService.GetIpAdr())
print(IP)


sleep(5)

Say("Welcome to Opensound!", Force=True)

while True:
    if AppService.Clients <= 0:
        Say(f"The Url is.  {IP} . colon 5 0 0 0 ",Force=True) # Says the IP
        sleep(15)
    else:
        sleep(15)

