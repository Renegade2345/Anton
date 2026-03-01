import os
from dotenv import load_dotenv

load_dotenv()

from vision_agents import Agent
from vision_agents import getstream
from vision_agents.processors import Processor
from vision_agents.plugins import openai

from ultralytics import YOLO

from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine
from threat_engine import ThreatEngine
from event_engine import EventEngine


class AntonProcessor(Processor):

    def __init__(self):
        super().__init__()

        self.model = YOLO("yolov8n.pt")

        self.state_engine = StateEngine()
        self.zone_engine = None
        self.watchlist_engine = WatchlistEngine()
        self.threat_engine = ThreatEngine()
        self.event_engine = EventEngine()

        self.frame_count = 0

    async def on_video(self, frame):

        self.frame_count += 1

        if self.zone_engine is None:
            h, w, _ = frame.shape
            self.zone_engine = ZoneEngine(w, h)

        if self.frame_count % 6 != 0:
            return

        results = self.model(frame)[0]

        detections = []

        for box in results.boxes:
            cls = int(box.cls[0])
            label = self.model.names[cls]

            x1, y1, x2, y2 = box.xyxy[0]

            detections.append({
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "label": label
            })

        objects = {str(i): d for i, d in enumerate(detections)}

        state_events = self.state_engine.update(objects)
        zone_events = self.zone_engine.update(objects)
        watchlist_events = self.watchlist_engine.update(objects)

        all_events = state_events + zone_events + watchlist_events

        self.event_engine.process_events(all_events)

        threat_levels = self.threat_engine.update(objects, all_events)

        if all_events:
            summary = [
                f"{e.get('label')} triggered {e.get('event')}"
                for e in all_events
            ]

            return {
                "text": f"Recon intelligence events detected: {summary}"
            }


def main():

    agent = Agent(
        edge=getstream.Edge(
            api_key=os.getenv("STREAM_API_KEY"),
            api_secret=os.getenv("STREAM_API_SECRET")
        ),
        instructions="You are ANTON, a military-grade reconnaissance AI.",
        processors=[AntonProcessor()],
        llm=openai.Realtime(fps=1)
    )

    print("ANTON running on Vision Agents Runtime...")

    agent.run()


if __name__ == "__main__":
    main()