class ZoneEngine:

    def __init__(self, frame_width, frame_height):

        # Define restricted zone (center rectangle)
        self.zone = {

            "x1": int(frame_width * 0.3),
            "y1": int(frame_height * 0.3),

            "x2": int(frame_width * 0.7),
            "y2": int(frame_height * 0.7),
        }

        self.alerted_objects = set()


    def is_inside_zone(self, bbox):

        x1, y1, x2, y2 = bbox

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        return (
            self.zone["x1"] <= cx <= self.zone["x2"] and
            self.zone["y1"] <= cy <= self.zone["y2"]
        )


    def update(self, tracked_objects):

        events = []

        for obj_id, data in tracked_objects.items():

            bbox = data["bbox"]
            label = data["label"]

            if self.is_inside_zone(bbox):

                if obj_id not in self.alerted_objects:

                    self.alerted_objects.add(obj_id)

                    events.append({
                        "event": "RESTRICTED_ZONE_ENTERED",
                        "id": obj_id,
                        "label": label
                    })

        return events


    def draw_zone(self, frame):

        x1 = self.zone["x1"]
        y1 = self.zone["y1"]

        x2 = self.zone["x2"]
        y2 = self.zone["y2"]

        import cv2

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            "RESTRICTED ZONE",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )