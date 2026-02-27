from vision_agents import Agent
from vision_agents import getstream
from vision_agents.plugins import openai
from vision_agents.processors import Processor

from ultralytics import YOLO

# Your existing intelligence modules
from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine
from threat_engine import ThreatEngine
from event_engine import EventEngine


class AntonProcessor(Processor):

    def __init__(self):
        super().__init__()

        # Vision Model
        self.model = YOLO("yolov8n.pt")

        # Intelligence Engines
        self.state_engine = StateEngine()
        self.zone_engine = None
        self.watchlist_engine = WatchlistEngine()
        self.threat_engine = ThreatEngine()
        self.event_engine = EventEngine()

        self.frame_count = 0


    async def on_video_frame(self, frame):

        self.frame_count += 1

        # Initialize zone engine once
        if self.zone_engine is None:
            h, w, _ = frame.shape
            self.zone_engine = ZoneEngine(w, h)

        # Frame skipping for performance
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

        # Convert detections to object format
        objects = {
            str(i): d for i, d in enumerate(detections)
        }

        # Run Intelligence Layers
        state_events = self.state_engine.update(objects)
        zone_events = self.zone_engine.update(objects)
        watchlist_events = self.watchlist_engine.update(objects)

        all_events = state_events + zone_events + watchlist_events

        # Process events (logging)
        self.event_engine.process_events(all_events)

        # Threat scoring
        threat_levels = self.threat_engine.update(objects, all_events)

        # Return text to Vision Agents LLM
        if all_events:

            summary = []
            for event in all_events:
                label = event.get("label", "object")
                ev = event.get("event", "activity")
                summary.append(f"{label} triggered {ev}")

            return {
                "text": f"Recon intelligence events detected: {summary}"
            }


def main():

    agent = Agent(
        edge=getstream.Edge(),  # Low-latency streaming
        instructions="You are ANTON, a military-grade reconnaissance AI.",
        processors=[AntonProcessor()],
        llm=openai.Realtime(fps=1)  # Native Vision Agents LLM plugin
    )

    print("ANTON running on Vision Agents Runtime...")

    agent.run()


if __name__ == "__main__":
    main()