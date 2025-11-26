import pyttsx3
import MusicService
import DataService
import threading
import queue


TTSEnabled = DataService.InternalSettings["TTSEnabled"]

# Use a queue to send speech tasks to a dedicated thread
TTSQueue = queue.Queue()
TTSThread: threading.Thread = None
SpeechVolume = 0.5


def TtsWorkerTask():
    TTSEngine = None
    try:
        TTSEngine = pyttsx3.init()
        TTSEngine.setProperty("rate",100)
    except RuntimeError:
        print("TTS Worker failed to initialize engine. TTS will be disabled.")
        return # Exit the thread
    
    while True:
        try:
            # Wait for the next speech task
            TextToSay = TTSQueue.get()

            if TextToSay is None:
                # A "None" item is our signal to stop the thread
                TTSQueue.task_done()
                break
            
            # We have a task, process it
            MusicService.AudioPlayer.volume = MusicService.SongInfo.MasterVolume / 2
            TTSEngine.say(TextToSay)
        
            TTSEngine.runAndWait()
            MusicService.AudioPlayer.volume = MusicService.SongInfo.MasterVolume
            
            TTSQueue.task_done()

        except Exception as e:
            print(f"Error in TtsWorkerTask: {e}")
            if TTSQueue.unfinished_tasks > 0:
                TTSQueue.task_done()

# Start the single, dedicated worker thread
# daemon=True means it will auto-exit when the main app closes
TTSThread = threading.Thread(target=TtsWorkerTask, daemon=True)
TTSThread.start()


if __name__ == "__main__":
    print("This is a module, and should not be run directly.")
    exit()

def Say(Text: str): 
    if not TTSEnabled: return   
    TTSQueue.put(Text)

def SayThenLog(Text: str):
    Say(Text)
    print(Text)