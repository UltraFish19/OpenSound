import pyttsx3
import MusicService
import DataService
import threading
import queue


TTSEnabled = False

# Use a queue to send speech tasks to a dedicated thread
TtsQueue = queue.Queue()
TtsThread: threading.Thread = None

TTSEnabled = True


def TtsWorkerTask():
    """A dedicated worker thread that handles all TTS requests from the queue."""
    TtsEngine = None
    try:
        TtsEngine = pyttsx3.init()
    except RuntimeError:
        print("TTS Worker failed to initialize engine. TTS will be disabled.")
        return # Exit the thread
    
    while True:
        try:
            # Wait for the next speech task
            TextToSay = TtsQueue.get()

            if TextToSay is None:
                # A "None" item is our signal to stop the thread
                TtsQueue.task_done()
                break
            
            # We have a task, process it
            MusicService.AudioPlayer.volume = 0.5
            TtsEngine.say(TextToSay)
            TtsEngine.runAndWait()
            MusicService.AudioPlayer.volume = 1.0
            
            TtsQueue.task_done()

        except Exception as e:
            print(f"Error in TtsWorkerTask: {e}")
            if TtsQueue.unfinished_tasks > 0:
                TtsQueue.task_done()

# Start the single, dedicated worker thread
# daemon=True means it will auto-exit when the main app closes
TtsThread = threading.Thread(target=TtsWorkerTask, daemon=True)
TtsThread.start()


if __name__ == "__main__":
    print("This is a module, and should not be run directly.")
    exit()

def Say(Text: str): 
    if not TTSEnabled: return   
    TtsQueue.put(Text)

def SayThenLog(Text: str):
    Say(Text)
    print(Text)