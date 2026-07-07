import yaml
import json
from parser import stream_logs
from features import FeatureEngine
from risk import RiskEngine
from mitigation import apply_mitigation

config = yaml.safe_load(open("../config/config.yaml"))
baseline = json.load(open("../data/baseline.json"))

feature_engine = FeatureEngine(config["window_size"])
risk_engine = RiskEngine(baseline, config["weights"])

THRESHOLD = config["threshold"]

def main():
    for event in stream_logs("../logs/pcf.log", "../logs/smf.log"):
        if not event:
            continue

        feature_engine.add_event(event)
        features = feature_engine.compute()

        intent = {imsi: 0.1 for imsi in features}

        risks = risk_engine.compute(features, intent)

        for imsi, score in risks.items():
            print(imsi, score)

            if score > THRESHOLD:
                apply_mitigation(imsi)

if __name__ == "__main__":
    main()
