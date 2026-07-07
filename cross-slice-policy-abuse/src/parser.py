import subprocess
import re
import time

def stream_logs(pcf_log, smf_log):
    proc = subprocess.Popen(
        ["tail", "-F", pcf_log, smf_log],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    while True:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield parse_line(line)

def parse_line(line):
    event = {}

    if "imsi-" in line:
        m = re.search(r'imsi-\d+', line)
        if m:
            event["imsi"] = m.group(0)

    if "Policy" in line:
        event["type"] = "pcf"

    elif "Session" in line:
        event["type"] = "smf"
        event["event"] = "modification"

    s = re.search(r'sst=(\d+),sd=([0-9A-Fa-f]+)', line)
    if s:
        event["slice"] = s.group(2)

    q = re.search(r'gbr=(\d+)', line)
    if q:
        event["qos"] = int(q.group(1))

    return event
