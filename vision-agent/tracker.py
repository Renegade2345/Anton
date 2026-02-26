import math
import uuid
import time


class Tracker:

    def __init__(self):

        self.objects = {}

        self.distance_threshold = 80   # increased tolerance
        self.max_disappeared_time = 1.5  # seconds


    def _calculate_center(self, bbox):

        x1, y1, x2, y2 = bbox

        return ((x1+x2)/2, (y1+y2)/2)


    def _calculate_distance(self, c1, c2):

        return math.sqrt(
            (c1[0]-c2[0])**2 +
            (c1[1]-c2[1])**2
        )


    def update(self, detections):

        current_time = time.time()

        matched_ids = set()

        # Match detections to existing objects
        for detection in detections:

            bbox = detection["bbox"]
            label = detection["label"]

            center = self._calculate_center(bbox)

            best_match = None
            best_distance = float("inf")

            for obj_id, obj in self.objects.items():

                if obj["label"] != label:
                    continue

                distance = self._calculate_distance(center, obj["center"])

                if distance < self.distance_threshold and distance < best_distance:

                    best_match = obj_id
                    best_distance = distance


            if best_match is None:

                best_match = str(uuid.uuid4())[:8]


            self.objects[best_match] = {
                "label": label,
                "bbox": bbox,
                "center": center,
                "last_seen": current_time
            }

            matched_ids.add(best_match)


        # Remove stale objects
        to_delete = []

        for obj_id, obj in self.objects.items():

            if current_time - obj["last_seen"] > self.max_disappeared_time:

                to_delete.append(obj_id)


        for obj_id in to_delete:

            del self.objects[obj_id]