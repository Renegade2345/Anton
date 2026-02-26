class AntonProcessor:

    def __init__(self):
        self.detector = Detector()
        self.tracker = Tracker()
        self.state_engine = StateEngine()
        self.watchlist_engine = WatchlistEngine()

    def process(self, frame):

        detections = self.detector.detect(frame)
        self.tracker.update(detections)

        events = []
        events.extend(self.state_engine.update(self.tracker.objects))
        events.extend(self.watchlist_engine.update(self.tracker.objects))

        return frame, events    