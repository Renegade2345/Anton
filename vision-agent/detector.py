from ultralytics import YOLO


class Detector:

    def __init__(self):

        self.model = YOLO("yolov8n.pt")

        self.allowed_classes = ["person", "car", "truck", "bus"]

        # Confidence threshold to reduce false positives
        self.confidence_threshold = 0.6


    def detect(self, frame):

        results = self.model(frame, verbose=False)

        detections = []

        for result in results:

            for box in result.boxes:

                confidence = float(box.conf[0])

                # Reject weak detections
                if confidence < self.confidence_threshold:
                    continue


                class_id = int(box.cls[0])
                label = self.model.names[class_id]

                if label not in self.allowed_classes:
                    continue


                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append({
                    "label": label,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence
                })

        return detections