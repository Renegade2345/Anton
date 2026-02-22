import cv2
from camera import Camera
from detector import Detector

def main():

    camera = Camera()
    detector = Detector()

    frame_count = 0

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        frame_count += 1

        # Frame skipping for real-time performance
        if frame_count % 6 == 0:

            detections = detector.detect(frame)

            for d in detections:

                x1, y1, x2, y2 = map(int, d["bbox"])
                label = d["label"]

                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0,255,0),
                    2
                )

        cv2.imshow("ARGUS - Vision Layer", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()


if __name__ == "__main__":
    main()