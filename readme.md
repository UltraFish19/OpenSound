# OpenSound


OpenSound is an open-source project that can allow anyone with a Raspberry PI (3+) to convert their PI into a smart speaker. The entire speaker focuses on privacy and can play music on YouTube without ads or any trackers.

---
## Features:

1. Searching and playing music on YouTube.
2. Simple and efficient interface
3. Raspberry PI friendly system
4. Favouriting Music 

---
## Requirements:
1. A Functioning Raspberry PI or Windows Computer
2. A Speaker (Optional but you probably need it)
3. Internet Connectivity
4. A device that can SSH onto a Raspberry PI (Optional)
5. Python 3.12 or above installed on device you wish to install on (Should be preinstalled on Raspberry PI, make sure for Windows that Python is added to PATH in order to make things easier)


---
## Installation:




#### Windows:

Installing on windows is relatively easy. First install the project, install the modules and lastly install FFMPEG.


```batch
pip install -r "<PATH TO Requirements.txt FILE>"
```

Next install ffmpeg from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip), extract it and place it somewhere easy to access.

Then go to `Editing the configuration` to configurate the project.

Finally run `OpenSound.py` to start.


### Raspberry PI:

Installing on Raspberry PI will take longer. The recommended installation is [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/).

> COMING SOON



#### Editing the configuration:

Both before starting the project you will need to first make changes to the `InternalSettings.json` file which is located in `OpenSound/Data/InternalSettings.json`


| Configuration | Description |
| ----------- | ----------- |
| MusicCacheLocation | This is where the music is stored, set this to any empty folder |
| FFMpegConverterLocation |This is only required for Windows installation set this to the `ffmpeg-x.x.x-essentials_build/ffmpeg-x.x.x-essentials_build/bin/ffmpeg.exe` |
| IsPI | Set this to `true` if you are installing on Raspberry PI |
| TTSEnabled | Set this to `true` if you want Text to Speech to announce any action you do such as play a song or favourite something   |


---
## Usage Guide:

If you set things up properly and run the project you will hear your device announce the IP Address of your speaker. Simply open a browser and type in the ip. It should look like this `192.168.53:5000` it might look different but make sure you type in an ip along side the port being `5000`.

To play music just press the button thats says `Music` and then you can search for songs. or go to `CURRENTURL/Music`.
