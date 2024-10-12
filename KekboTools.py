import json
import os

def running_in_docker():
    if os.path.exists("/.dockerenv"):
        return True
    try:
        with open("/proc/1/cgroup", "rt") as f:
            for line in f:
                if "docker" in line:
                    return True
    except FileNotFoundError:
        pass
    return False


def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False