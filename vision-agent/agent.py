import cv2
from camera import Camera
from detector import Detector
from tracker import Tracker


def main():

    # Initialize core components
    camera = Camera()
    detector = Detector()
    tracker = Tracker()

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

            # Update tracker with detections
            tracker.update(detections)

        # Draw tracked objects (NOT raw detections)
        for obj_id, data in tracker.objects.items():

            x1, y1, x2, y2 = map(int, data["bbox"])
            label = data["label"]

            display_text = f"{label} [{obj_id}]"

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Draw label + persistent ID
            cv2.putText(
                frame,
                display_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        # Show output
        cv2.imshow("ANTON - Tracking Layer", frame)

        # Exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    camera.release()


if __name__ == "__main__":
    main()