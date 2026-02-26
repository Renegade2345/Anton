import cv2
from camera import Camera
from detector import Detector
from tracker import Tracker
from state_engine import StateEngine   # REQUIRED


def main():

    # Initialize core components
    camera = Camera()
    detector = Detector()
    tracker = Tracker()
    state_engine = StateEngine()   # REQUIRED

    frame_count = 0

    while True:

        # Read frame
        ret, frame = camera.read()

        if not ret:
            break

        frame_count += 1

        # Run detection every 6th frame (performance optimization)
        if frame_count % 6 == 0:

            detections = detector.detect(frame)

            # Update tracker
            tracker.update(detections)

            # Update state engine (behavior intelligence)
            events = state_engine.update(tracker.objects)

            # Print intelligence events
            for event in events:
                print(event)


        # Draw tracked objects
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


        cv2.imshow("ANTON - Intelligence Layer", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    camera.release()


if __name__ == "__main__":
    main()