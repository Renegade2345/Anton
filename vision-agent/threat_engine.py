class ThreatEngine:

    def __init__(self):
        self.current_threat = 0.0
        self.decay_rate = 0.02 
        self.max_threat = 1.0

    def update(self, objects, events):

        threat_score = self.current_threat

        # Base object presence adds small threat
        threat_score += 0.01 * len(objects)

        for event in events:

            event_type = event.get("event", "")
            label = event.get("label", "")

            # Zone breach = moderate escalation
            if "ZONE" in event_type:
                threat_score += 0.2

            # Watchlist match = heavy escalation
            if "WATCHLIST" in event_type:
                threat_score += 0.5

            # Suspicious state detection
            if "SUSPICIOUS" in event_type:
                threat_score += 0.3

        # Apply decay so threat slowly drops
        threat_score -= self.decay_rate

        # Clamp between 0 and max
        threat_score = max(0.0, min(self.max_threat, threat_score))

        self.current_threat = threat_score

        return self.current_threat