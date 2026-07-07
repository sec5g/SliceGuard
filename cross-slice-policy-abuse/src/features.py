from collections import defaultdict
import time

class FeatureEngine:
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.buffer = []

    def add_event(self, event):
        event["ts"] = time.time()
        self.buffer.append(event)
        self.cleanup()

    def cleanup(self):
        now = time.time()
        self.buffer = [e for e in self.buffer if now - e["ts"] <= self.window_size]

    def compute(self):
        grouped = defaultdict(list)

        for e in self.buffer:
            if "imsi" in e:
                grouped[e["imsi"]].append(e)

        features = {}

        for imsi, ev in grouped.items():
            f_mod = sum(1 for e in ev if e.get("event") == "modification")
            f_pcf = sum(1 for e in ev if e.get("type") == "pcf")

            qos_vals = [e.get("qos", 0) for e in ev]
            delta_qos = max(qos_vals) - min(qos_vals) if qos_vals else 0

            slices = set(e.get("slice") for e in ev if "slice" in e)

            features[imsi] = {
                "f_mod": f_mod,
                "f_pcf": f_pcf,
                "delta_qos": delta_qos,
                "f_slice": len(slices) / max(len(ev), 1)
            }

        return features
