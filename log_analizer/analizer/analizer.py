import re
import json
from typing import Optional, Dict, List, Set
from collections import defaultdict


# ==============================
# REGEX PATTERNS
# ==============================

LOG_PATTERN = re.compile(
    r"(?P<date>\d{6})\s+(?P<time>\d{6})\s+(?P<thread>\d+)\s+"
    r"(?P<level>\w+)\s+(?P<component>[^:]+):\s+(?P<message>.*)"
)

IP_PATTERN = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
BLOCK_PATTERN = re.compile(r"blk_-?\d+")

# ==============================
# PARSER
# ==============================

def parse_line(line: str) -> Optional[Dict]:
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    return match.groupdict()


def parse_message(data: Dict) -> Dict:
    message = data["message"]

    # Extract ALL IPs (important upgrade)
    ips = IP_PATTERN.findall(message)
    if ips:
        data["ips"] = ips

    # Extract block id
    block_match = BLOCK_PATTERN.search(message)
    if block_match:
        data["block_id"] = block_match.group()

    # Event classification
    if "Receiving block" in message:
        data["event_type"] = "RECEIVE_START"
    elif "Received block" in message:
        data["event_type"] = "RECEIVE_COMPLETE"
    elif "allocateBlock" in message:
        data["event_type"] = "ALLOCATE"
    elif "addStoredBlock" in message:
        data["event_type"] = "STORE"
    else:
        data["event_type"] = "UNKNOWN"

    return data


# ==============================
# ANALYZER
# ==============================

class Analyzer:
    def __init__(self):
        self.total_lines: int = 0
        self.level_count: Dict[str, int] = defaultdict(int)
        self.ip_count: Dict[str, int] = defaultdict(int)

        self.block_tracker: Dict[str, Dict] = {}
        self.anomalies: List[Dict] = []

    # --------------------------
    # MAIN PROCESS FUNCTION
    # --------------------------
    def process(self, data: Dict):
        self.total_lines += 1

        # Count log levels
        self.level_count[data["level"]] += 1

        # Count IPs
        for ip in data.get("ips", []):
            self.ip_count[ip] += 1

        # Track blocks
        self.track_block(data)

        # Detect anomalies
        self.detect(data)

    # --------------------------
    # BLOCK TRACKING
    # --------------------------
    def track_block(self, data: Dict):
        block_id = data.get("block_id")
        if not block_id:
            return

        if block_id not in self.block_tracker:
            self.block_tracker[block_id] = {
                "receive_start": 0,
                "receive_complete": 0,
                "store": 0,
                "sources": set()
            }

        block = self.block_tracker[block_id]

        if data["event_type"] == "RECEIVE_START":
            block["receive_start"] += 1

        elif data["event_type"] == "RECEIVE_COMPLETE":
            block["receive_complete"] += 1

        elif data["event_type"] == "STORE":
            block["store"] += 1

        # Track IP sources
        for ip in data.get("ips", []):
            block["sources"].add(ip)

    # --------------------------
    # ANOMALY DETECTION
    # --------------------------
    def detect(self, data: Dict):
        # Unknown log level
        if data["level"] not in ["INFO", "WARN", "ERROR"]:
            self.anomalies.append({
                "type": "UNKNOWN_LEVEL",
                "data": data
            })

        # External IP detection
        for ip in data.get("ips", []):
            if not self.is_internal_ip(ip):
                self.anomalies.append({
                    "type": "EXTERNAL_IP",
                    "ip": ip
                })

    # --------------------------
    # FINAL CHECKS
    # --------------------------
    def finalize(self):
        for block_id, block in self.block_tracker.items():
            if block["receive_start"] != block["receive_complete"]:
                self.anomalies.append({
                    "type": "INCOMPLETE_BLOCK_TRANSFER",
                    "block_id": block_id,
                    "details": block
                })

            if block["store"] == 0:
                self.anomalies.append({
                    "type": "BLOCK_NOT_STORED",
                    "block_id": block_id
                })

    # --------------------------
    # HELPERS
    # --------------------------
    @staticmethod
    def is_internal_ip(ip: str) -> bool:
        return ip.startswith(("10.", "172.", "192.168."))


