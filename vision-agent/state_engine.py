import time


class StateEngine:

    def __init__(self):

        self.object_states = {}

        # seconds before object considered exited
        self.exit_timeout = 2.0

        # seconds before loitering alert
        self.loitering_threshold = 10.0


    def update(self, tracked_objects):

        current_time = time.time()

        events = []

        current_ids = set()

        for obj_id, data in tracked_objects.items():

            label = data["label"]

            current_ids.add(obj_id)

            # New object detected
            if obj_id not in self.object_states:

                self.object_states[obj_id] = {
                    "label": label,
                    "first_seen": current_time,
                    "last_seen": current_time,
                    "loitering_alerted": False
                }

                events.append({
                    "event": "OBJECT_ENTERED",
                    "id": obj_id,
                    "label": label,
                    "timestamp": round(current_time, 2)
                })

            else:

                state = self.object_states[obj_id]

                state["last_seen"] = current_time

                duration = current_time - state["first_seen"]

                # Loitering detection
                if (
                    duration >= self.loitering_threshold and
                    not state["loitering_alerted"]
                ):

                    state["loitering_alerted"] = True

                    events.append({
                        "event": "LOITERING_DETECTED",
                        "id": obj_id,
                        "label": label,
                        "duration": round(duration, 2)
                    })


        # Detect exited objects
        to_remove = []

        for obj_id, state in self.object_states.items():

            if obj_id not in current_ids:

                if current_time - state["last_seen"] >= self.exit_timeout:

                    duration = current_time - state["first_seen"]

                    events.append({
                        "event": "OBJECT_EXITED",
                        "id": obj_id,
                        "label": state["label"],
                        "duration": round(duration, 2)
                    })

                    to_remove.append(obj_id)


        for obj_id in to_remove:

            del self.object_states[obj_id]


        return events