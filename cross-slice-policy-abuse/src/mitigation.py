import os

def apply_mitigation(imsi):
    print(f"[MITIGATION] Limiting UE {imsi}")
    os.system("tc qdisc replace dev ogstun root tbf rate 50mbit burst 32k latency 400ms")
