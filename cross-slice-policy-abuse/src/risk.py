import json

class RiskEngine:
    def __init__(self, baseline, weights, alpha=0.2):
        self.baseline = baseline
        self.weights = weights
        self.ewma = {}
        self.alpha = alpha

    def z(self, x, mean, std):
        return (x - mean) / std if std > 0 else 0

    def compute(self, features, intent):
        risks = {}

        for imsi, f in features.items():
            z_mod = self.z(f["f_mod"], self.baseline["f_mod"]["mean"], self.baseline["f_mod"]["std"])
            z_pcf = self.z(f["f_pcf"], self.baseline["f_pcf"]["mean"], self.baseline["f_pcf"]["std"])
            z_qos = self.z(f["delta_qos"], self.baseline["delta_qos"]["mean"], self.baseline["delta_qos"]["std"])
            z_slice = self.z(f["f_slice"], self.baseline["f_slice"]["mean"], self.baseline["f_slice"]["std"])

            R = (
                self.weights["w_mod"] * z_mod +
                self.weights["w_pcf"] * z_pcf +
                self.weights["w_qos"] * z_qos +
                self.weights["w_slice"] * z_slice +
                self.weights["w_intent"] * intent.get(imsi, 0)
            )

            prev = self.ewma.get(imsi, R)
            ewma_val = self.alpha * R + (1 - self.alpha) * prev

            self.ewma[imsi] = ewma_val
            risks[imsi] = ewma_val

        return risks
