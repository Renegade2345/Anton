import math
import uuid


class Tracker:

    def __init__(self):

        # Stores active tracked objects
        self.objects = {}

        # Distance threshold to consider same object
        self.distance_threshold = 50


    def _calculate_center(self, bbox):

        x1, y1, x2, y2 = bbox

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        return (cx, cy)


    def _calculate_distance(self, c1, c2):

        return math.sqrt(
            (c1[0] - c2[0])**2 +
            (c1[1] - c2[1])**2
        )


    def update(self, detections):

        tracked = []

        for detection in detections:

            bbox = detection["bbox"]
            label = detection["label"]

            center = self._calculate_center(bbox)

            matched_id = None

            # Try matching existing objects
            for obj_id, obj in self.objects.items():

                if obj["label"] != label:
                    continue

                dist = self._calculate_distance(
                    center,
                    obj["center"]
                )

                if dist < self.distance_threshold:

                    matched_id = obj_id
                    break


            # If no match, create new object
            if matched_id is None:

                matched_id = str(uuid.uuid4())[:8]


            # Update object state
            self.objects[matched_id] = {
                "label": label,
                "bbox": bbox,
                "center": center
            }

            tracked.append({
                "id": matched_id,
                "label": label,
                "bbox": bbox
            })


        return tracked