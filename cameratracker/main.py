import tracker
import threading
class App:
    def __init__(self):
        track = tracker.Tracker()
        track_thread = threading.Thread(target=track.track_video)
        track_thread.start()
        track.toggle_video()
        




if __name__ == "__main__":
    app = App()