import cv2

from camera import Camera
from detector import Detector
from tracker import Tracker
from state_engine import StateEngine
from zone_engine import ZoneEngine
from watchlist_engine import WatchlistEngine


def main():

    # Initialize core components
    camera = Camera()
    detector = Detector()
    tracker = Tracker()
    state_engine = StateEngine()

    frame_count = 0

    # Read first frame to initialize zone and watchlist engines
    ret, frame = camera.read()

    if not ret:
        print("Failed to read camera")
        return

    frame_height, frame_width, _ = frame.shape

    zone_engine = ZoneEngine(frame_width, frame_height)
    watchlist_engine = WatchlistEngine()

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        frame_count += 1

        # Run detection every 6th frame (performance optimization)
        if frame_count % 6 == 0:

            # Step 1: Detect objects
            detections = detector.detect(frame)

            # Step 2: Update tracker (persistent identity)
            tracker.update(detections)

            # Step 3: Behavioral intelligence (entry, exit, loitering)
            state_events = state_engine.update(tracker.objects)

            for event in state_events:
                print(event)

            # Step 4: Restricted zone intelligence
            zone_events = zone_engine.update(tracker.objects)

            for event in zone_events:
                print(event)

            # Step 5: Watchlist intelligence
            watchlist_events = watchlist_engine.update(tracker.objects)

            for event in watchlist_events:
                print(event)


        # Draw restricted zone overlay
        zone_engine.draw_zone(frame)


        # Draw tracked objects with IDs
        for obj_id, data in tracker.objects.items():

            x1, y1, x2, y2 = map(int, data["bbox"])
            label = data["label"]

            display_text = f"{label} [{obj_id}]"

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                display_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )


        # Show Anton intelligence system output
        cv2.imshow("ANTON - Recon Intelligence System", frame)


        # Exit on Q key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Cleanup resources
    camera.release()


if __name__ == "__main__":
    main()