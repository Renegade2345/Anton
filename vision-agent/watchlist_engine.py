class WatchlistEngine:

    def __init__(self):

        # Define watchlist targets
        self.watchlist = {

            "person": True,
            "car": True,

            # can extend later
            # "truck": True
        }

        # Track already alerted objects
        self.alerted_ids = set()


    def update(self, tracked_objects):

        events = []

        for obj_id, data in tracked_objects.items():

            label = data["label"]

            if label in self.watchlist:

                if obj_id not in self.alerted_ids:

                    self.alerted_ids.add(obj_id)

                    events.append({
                        "event": "WATCHLIST_MATCH",
                        "id": obj_id,
                        "label": label
                    })

        return events