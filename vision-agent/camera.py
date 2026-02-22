import cv2

class Camera:

    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            raise Exception("Camera could not be opened")

    def read(self):
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        self.cap.release()  
        cv2.destroyAllWindows()