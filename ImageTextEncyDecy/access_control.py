# File: access_control.py

import json
import os
from datetime import datetime

LOG_FILE = "data/access_log.json"
KEY_FILE = "keys/access_keys.json"
REQUEST_FILE = "data/requests.json"

def ensure_files():
    os.makedirs("data/encrypted", exist_ok=True)
    os.makedirs("data/decrypted", exist_ok=True)
    os.makedirs("keys", exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "w") as f:
            json.dump({}, f)

    if not os.path.exists(REQUEST_FILE):
        with open(REQUEST_FILE, "w") as f:
            json.dump({}, f)

def log_access(owner, filename, shared_with):
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append({
        "owner": owner,
        "filename": filename,
        "shared_with": shared_with,
        "timestamp": datetime.now().isoformat()
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def grant_access(filename, username, key_hex):
    with open(KEY_FILE, "r") as f:
        keys = json.load(f)

    if filename not in keys:
        keys[filename] = {}

    keys[filename][username] = key_hex

    with open(KEY_FILE, "w") as f:
        json.dump(keys, f, indent=2)

def get_key_if_allowed(filename, username):
    with open(KEY_FILE, "r") as f:
        keys = json.load(f)

    if filename in keys and username in keys[filename]:
        return keys[filename][username]
    else:
        return None

def view_log():
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def request_access(filename, username):
    with open(REQUEST_FILE, "r") as f:
        requests = json.load(f)
    if filename not in requests:
        requests[filename] = []
    if username not in requests[filename]:
        requests[filename].append(username)
    with open(REQUEST_FILE, "w") as f:
        json.dump(requests, f, indent=2)

def get_requests():
    with open(REQUEST_FILE, "r") as f:
        return json.load(f)

def clear_request(filename, username):
    with open(REQUEST_FILE, "r") as f:
        requests = json.load(f)
    if filename in requests and username in requests[filename]:
        requests[filename].remove(username)
        if not requests[filename]:
            del requests[filename]
    with open(REQUEST_FILE, "w") as f:
        json.dump(requests, f, indent=2)
