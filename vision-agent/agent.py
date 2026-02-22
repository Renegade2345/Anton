import cv2
from camera import Camera

def main():

    camera = Camera()

    frame_count = 0

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        frame_count += 1

        # Show feed
        cv2.imshow("ANTON - Live Feed", frame)

        # Quit on Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()


if __name__ == "__main__":
    main()