# microservice 3 server.py

# simple ZMQ implementation -- no databases.

import json
import time
from datetime import datetime, timezone
import zmq

# database workaround -- create a local list to store calls

event_log = {}

# App Whitelist -- update this list with your App Name -- make sure your calls match this
WHITELIST = {"TaskTracker", "FitnessApp", "HabitTracker"}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("[microservice 3] listening on tcp://*:5555")


# USER STORY 1: generate timestamp
def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

# USER STORY #: generate response for ping
def pong():
    return {"status": 200, "message": "pong"}

# USER STORY 1: return timestamp
def return_timestamp(payload):
    # get vals for clientID and eventName
    client_id = payload.get("clientID")
    event_name = payload.get("eventName")

    # check for missing clientID 
    if not client_id:
        return {"status": 400, "error": "invalid or missing field: clientID"}
    # check if clientID is string
    if not isinstance(client_id, str):
        return {"status": 400, "error": "invalid or missing field: clientID"}
    
    # check if clientID is in whitelist
    if client_id not in WHITELIST:
        return {"status": 401, "error": "clientID is not a whitelisted APP"}

    # check for missing eventName 
    if not event_name:
        return {"status": 400, "error": "invalid or missing field: eventName"}
    # check if eventName is string
    if not isinstance(event_name, str):
        return {"status": 400, "error": "invalid or missing field: eventName"}
    
    key = (client_id, event_name)

    event_timestamp = timestamp()
    event_log.setdefault(client_id, []).append({"eventName": event_name, "timestamp": event_timestamp})

    return {"status": 200, "message": "timestamp", "timestamp": event_timestamp}


    

# identify request from listener
def create_response(payload):
    action = payload.get("action")
    # check that action was defined
    if not action:
        return {"status": 400, "error": "invalid or missing field: action"}

    if action == "ping":
        return pong()
    
    if action == "timestamp":
        return return_timestamp(payload)


# main loop
while True:
    message = socket.recv()
    text = message.decode("utf-8")
    print(f"[microservice 3] received: {text}")
    # copied from ZMQ
    if text == "Q":
        socket.send_string(json.dumps({"status": 200, "message": "bye"}))
        break

    payload = json.loads(text)

    response = create_response(payload)

    time.sleep(0.2)

    socket.send_string(json.dumps(response))

context.destroy()
print("[microservice 3] stopped")