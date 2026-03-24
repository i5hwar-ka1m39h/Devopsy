
import re
from typing import Optional, Dict
import os
import json
file_path = "./../hdfs.log"




LOG_PATTERN = re.compile(
    r"(?P<date>\d{6})\s+(?P<time>\d{6})\s+(?P<thread>\d+)\s+"
    r"(?P<level>\w+)\s+(?P<component>[^:]+):\s+(?P<message>.*)"
)

def parse_line(line: str) -> Optional[Dict]:
    match = LOG_PATTERN.match(line)
    if not match:
        return None  # unknown format
    
    return match.groupdict()

def parse_message(data:Dict)->Dict:
    message = data["message"]

    match = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", data["message"])
    if match:
        data["ip_addr"] = match.group()


    if "Receiving block" in message:
        data["event_type"] = "RECEIVE_START"

    elif "Received block" in message:
        data["event_type"] = "RECEIVE_COMPLETE"

    elif "allocateBlock" in message:
        data["event_type"] = "ALLOCATE"

    else:
        data["event_type"] = "UNKNOWN"

    return data

def main_parser():
    
    # print( os.path.exists(file_path))
    ip_set = set()



    with open(file_path,"r") as f:
        
        for line in f:
            json_response = parse_line(line)
            if not json_response:
                break
            data = parse_message(json_response)
            match = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", data["message"])
            if match:
                ip_set.add(match.group())
            print(json.dumps(data))
            
    # print("ip set is ====>", ip_set, "\nlenght of the set is: ")

main_parser()