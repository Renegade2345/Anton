import cv2
from ultralytics import YOLO

from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine
from threat_engine import ThreatEngine
from event_engine import EventEngine


class AntonEngine:

    def __init__(self):

        self.model = YOLO("yolov8n.pt")

        self.state_engine = StateEngine()
        self.zone_engine = None
        self.watchlist_engine = WatchlistEngine()
        self.threat_engine = ThreatEngine()
        self.event_engine = EventEngine()

        self.frame_count = 0

    def process_frame(self, frame):

        self.frame_count += 1
        events_output = []

        if self.zone_engine is None:
            h, w, _ = frame.shape
            self.zone_engine = ZoneEngine(w, h)

        # Frame skipping for performance
        if self.frame_count % 6 != 0:
            return frame, self.threat_engine.current_threat, events_output

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

            # Draw box
            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        objects = {str(i): d for i, d in enumerate(detections)}

        state_events = self.state_engine.update(objects)
        zone_events = self.zone_engine.update(objects)
        watchlist_events = self.watchlist_engine.update(objects)

        all_events = state_events + zone_events + watchlist_events

        self.event_engine.process_events(all_events)
        threat_level = self.threat_engine.update(objects, all_events)

        for e in all_events:
            events_output.append(f"{e.get('label')} → {e.get('event')}")

        # Draw threat level on frame
        cv2.putText(
            frame,
            f"Threat: {threat_level:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        return frame, threat_level, events_output


# Global engine instance for dashboard usage
anton_engine = AntonEngine()


def run_anton_frame(frame):
    return anton_engine.process_frame(frame)