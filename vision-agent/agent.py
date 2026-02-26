import cv2

from camera import Camera
from detector import Detector
from tracker import Tracker
from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine
from event_engine import EventEngine
from threat_engine import ThreatEngine
from llm_engine import LLMEngine


def main():

    # -----------------------------
    # Initialize Core Components
    # -----------------------------
    camera = Camera()
    detector = Detector()
    tracker = Tracker()

    state_engine = StateEngine()
    watchlist_engine = WatchlistEngine()
    event_engine = EventEngine()
    threat_engine = ThreatEngine()
    llm_engine = LLMEngine()

    frame_count = 0
    threat_levels = {}

    # Read first frame to initialize zone engine
    ret, frame = camera.read()

    if not ret:
        print("Camera initialization failed.")
        return

    frame_height, frame_width, _ = frame.shape
    zone_engine = ZoneEngine(frame_width, frame_height)

    print("\nANTON Recon Intelligence System Started\n")

    # -----------------------------
    # Main Loop
    # -----------------------------
    while True:

        ret, frame = camera.read()

        if not ret:
            break

        frame_count += 1

        all_events = []

        # -----------------------------
        # Detection + Intelligence (every 6 frames)
        # -----------------------------
        if frame_count % 6 == 0:

            # Detection
            detections = detector.detect(frame)

            # Tracking
            tracker.update(detections)

            # Intelligence engines
            state_events = state_engine.update(tracker.objects)
            zone_events = zone_engine.update(tracker.objects)
            watchlist_events = watchlist_engine.update(tracker.objects)

            # Combine events
            all_events.extend(state_events)
            all_events.extend(zone_events)
            all_events.extend(watchlist_events)

            # Process alerts
            event_engine.process_events(all_events)

            # Threat scoring
            threat_levels = threat_engine.update(
                tracker.objects,
                all_events
            )

            # -----------------------------
            # LLM Intelligence (Cooldown)
            # Runs every 120 frames (~4 sec)
            # -----------------------------
            if all_events and frame_count % 120 == 0:

                analysis = llm_engine.analyze(
                    tracker.objects,
                    all_events,
                    threat_levels
                )

                if analysis:
                    print("\n[ANTON INTELLIGENCE REPORT]")
                    print(analysis)
                    print()


        # -----------------------------
        # Draw Restricted Zone
        # -----------------------------
        zone_engine.draw_zone(frame)


        # -----------------------------
        # Draw Tracked Objects
        # -----------------------------
        for obj_id, data in tracker.objects.items():

            x1, y1, x2, y2 = map(int, data["bbox"])
            label = data["label"]
            threat = threat_levels.get(obj_id, "LOW")

            display_text = f"{label} [{obj_id}] ({threat})"

            # Threat Color Coding
            if threat == "LOW":
                color = (0, 255, 0)
            elif threat == "MEDIUM":
                color = (0, 255, 255)
            elif threat == "HIGH":
                color = (0, 165, 255)
            else:
                color = (0, 0, 255)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            cv2.putText(
                frame,
                display_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )


        # -----------------------------
        # Display
        # -----------------------------
        cv2.imshow(
            "ANTON - Recon Intelligence System",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # -----------------------------
    # Cleanup
    # -----------------------------
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()