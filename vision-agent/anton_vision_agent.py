import cv2

from vision_agents import Agent
from vision_agents.processors import VideoProcessor

from detector import Detector
from tracker import Tracker
from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine
from event_engine import EventEngine
from threat_engine import ThreatEngine


class AntonProcessor(VideoProcessor):

    def __init__(self):

        super().__init__()

        self.detector = Detector()
        self.tracker = Tracker()
        self.state_engine = StateEngine()
        self.watchlist_engine = WatchlistEngine()
        self.event_engine = EventEngine()
        self.threat_engine = ThreatEngine()

        self.zone_engine = None
        self.frame_count = 0
        self.threat_levels = {}


    def process_frame(self, frame):

        if self.zone_engine is None:

            height, width, _ = frame.shape
            self.zone_engine = ZoneEngine(width, height)


        self.frame_count += 1

        if self.frame_count % 6 == 0:

            detections = self.detector.detect(frame)

            self.tracker.update(detections)

            state_events = self.state_engine.update(self.tracker.objects)
            zone_events = self.zone_engine.update(self.tracker.objects)
            watchlist_events = self.watchlist_engine.update(self.tracker.objects)

            all_events = []
            all_events.extend(state_events)
            all_events.extend(zone_events)
            all_events.extend(watchlist_events)

            self.event_engine.process_events(all_events)

            self.threat_levels = self.threat_engine.update(
                self.tracker.objects,
                all_events
            )


        self.zone_engine.draw_zone(frame)

        for obj_id, data in self.tracker.objects.items():

            x1, y1, x2, y2 = map(int, data["bbox"])
            label = data["label"]

            threat = self.threat_levels.get(obj_id, "LOW")

            display_text = f"{label} [{obj_id}] ({threat})"

            if threat == "LOW":
                color = (0, 255, 0)
            elif threat == "MEDIUM":
                color = (0, 255, 255)
            elif threat == "HIGH":
                color = (0, 165, 255)
            else:
                color = (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            cv2.putText(
                frame,
                display_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

        return frame


def main():

    processor = AntonProcessor()

    agent = Agent(
        instructions="You are ANTON, a real-time reconnaissance intelligence agent.",
        processors=[processor]
    )

    print("ANTON Vision Agent started")

    agent.run()


if __name__ == "__main__":
    main()