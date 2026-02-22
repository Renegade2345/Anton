from ultralytics import YOLO

class Detector:

    def __init__(self):

        # Load lightweight real-time model
        self.model = YOLO("yolov8n.pt")

        # Only track relevant classes
        self.allowed_classes = ["person", "car", "truck", "bus"]

    def detect(self, frame):

        results = self.model(frame, verbose=False)

        detections = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])
                label = self.model.names[class_id]

                if label not in self.allowed_classes:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append({
                    "label": label,
                    "bbox": [x1, y1, x2, y2]
                })

        return detections