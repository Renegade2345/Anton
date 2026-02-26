import time
import json
import os


class EventEngine:

    def __init__(self):

        self.event_history = []
        self.alerted_recently = {}

        os.makedirs("logs", exist_ok=True)

        self.log_file = "logs/anton_events.json"


    def process_events(self, events):

        for event in events:

            if self._should_alert(event):

                self._trigger_alert(event)

                self._log_event(event)


    def _should_alert(self, event):

        event_key = f"{event['event']}_{event.get('id', '')}"

        current_time = time.time()

        if event_key in self.alerted_recently:

            if current_time - self.alerted_recently[event_key] < 5:
                return False

        self.alerted_recently[event_key] = current_time

        return True


    def _trigger_alert(self, event):

        print("\n[ALERT]", json.dumps(event, indent=2))


    def _log_event(self, event):

        event["timestamp"] = time.time()

        self.event_history.append(event)

        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")