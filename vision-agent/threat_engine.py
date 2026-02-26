class ThreatEngine:

    def __init__(self):

        self.threat_scores = {}


    def update(self, tracked_objects, events):

        threat_levels = {}

        # Reset scores
        for obj_id in tracked_objects:

            if obj_id not in self.threat_scores:
                self.threat_scores[obj_id] = 0

            label = tracked_objects[obj_id]["label"]

            if label == "person":
                self.threat_scores[obj_id] += 10

            elif label in ["car", "truck"]:
                self.threat_scores[obj_id] += 15


        # Add event-based scoring
        for event in events:

            obj_id = event.get("id")

            if obj_id is None:
                continue

            if event["event"] == "WATCHLIST_MATCH":
                self.threat_scores[obj_id] += 50

            elif event["event"] == "RESTRICTED_ZONE_ENTERED":
                self.threat_scores[obj_id] += 40

            elif event["event"] == "LOITERING_DETECTED":
                self.threat_scores[obj_id] += 30


        # Convert score → threat level
        for obj_id, score in self.threat_scores.items():

            if score >= 70:
                threat_levels[obj_id] = "CRITICAL"

            elif score >= 40:
                threat_levels[obj_id] = "HIGH"

            elif score >= 20:
                threat_levels[obj_id] = "MEDIUM"

            else:
                threat_levels[obj_id] = "LOW"


        return threat_levels