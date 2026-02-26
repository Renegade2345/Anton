import cv2

from camera import Camera
from detector import Detector
from tracker import Tracker
from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine
from event_engine import EventEngine
from threat_engine import ThreatEngine


def main():

    # Initialize core components
    camera = Camera()
    detector = Detector()
    tracker = Tracker()
    state_engine = StateEngine()

    frame_count = 0

    # Read first frame to initialize zone engine
    ret, frame = camera.read()

    if not ret:
        print("Failed to read camera")
        return

    frame_height, frame_width, _ = frame.shape

    zone_engine = ZoneEngine(frame_width, frame_height)
    watchlist_engine = WatchlistEngine()
    event_engine = EventEngine()
    threat_engine = ThreatEngine()

    threat_levels = {}

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        frame_count += 1

        # Run detection every 6 frames (performance optimization)
        if frame_count % 6 == 0:

            # Step 1 — Detect
            detections = detector.detect(frame)

            # Step 2 — Track
            tracker.update(detections)

            # Step 3 — Behavioral intelligence
            state_events = state_engine.update(tracker.objects)

            # Step 4 — Zone intelligence
            zone_events = zone_engine.update(tracker.objects)

            # Step 5 — Watchlist intelligence
            watchlist_events = watchlist_engine.update(tracker.objects)

            # Step 6 — Combine all events
            all_events = []
            all_events.extend(state_events)
            all_events.extend(zone_events)
            all_events.extend(watchlist_events)

            # Step 7 — Process alerts and logging
            event_engine.process_events(all_events)

            # Step 8 — Threat scoring
            threat_levels = threat_engine.update(
                tracker.objects,
                all_events
            )


        # Draw restricted zone
        zone_engine.draw_zone(frame)


        # Draw tracked objects with threat level
        for obj_id, data in tracker.objects.items():

            x1, y1, x2, y2 = map(int, data["bbox"])
            label = data["label"]

            threat = threat_levels.get(obj_id, "LOW")

            display_text = f"{label} [{obj_id}] ({threat})"

            # Threat color coding
            if threat == "LOW":
                color = (0, 255, 0)

            elif threat == "MEDIUM":
                color = (0, 255, 255)

            elif threat == "HIGH":
                color = (0, 165, 255)

            else:  # CRITICAL
                color = (0, 0, 255)


            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # Draw label text
            cv2.putText(
                frame,
                display_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )


        # Display Anton interface
        cv2.imshow(
            "ANTON - Recon Intelligence System",
            frame
        )


        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Cleanup
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()