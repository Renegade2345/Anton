from vision_agents.core.agent import Agent
from vision_agents.core.edge.local import LocalEdge

from detector import Detector
from tracker import Tracker
from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine

import cv2


class AntonVisionProcessor:

    def __init__(self):

        self.detector = Detector()
        self.tracker = Tracker()
        self.state_engine = StateEngine()

        self.zone_engine = None
        self.watchlist_engine = WatchlistEngine()

        self.initialized = False


    def process(self, frame):

        if not self.initialized:

            h, w, _ = frame.shape
            self.zone_engine = ZoneEngine(w, h)
            self.initialized = True


        detections = self.detector.detect(frame)

        self.tracker.update(detections)

        events = []

        events.extend(self.state_engine.update(self.tracker.objects))
        events.extend(self.zone_engine.update(self.tracker.objects))
        events.extend(self.watchlist_engine.update(self.tracker.objects))

        for event in events:
            print("[ANTON INTEL]", event)


        self.zone_engine.draw_zone(frame)

        for obj_id, data in self.tracker.objects.items():

            x1, y1, x2, y2 = map(int, data["bbox"])

            label = data["label"]

            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

            cv2.putText(
                frame,
                f"{label} [{obj_id}]",
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                2
            )

        return frame


def main():

    processor = AntonVisionProcessor()

    agent = Agent(
        edge=LocalEdge(),
        instructions="Anton Recon Intelligence Agent"
    )

    print("Anton Vision Agent started")

    agent.run(processor.process)


if __name__ == "__main__":
    main()