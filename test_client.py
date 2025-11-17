# microservice test client 

import json
import zmq
import time

context = zmq.Context()
print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Sending a request...")


# call function -- what we use to communicate to server
def call(object):
    socket.send_string(json.dumps(object))
    print("REQUEST :", object)
    # Message Contract -- Server Reply:
    response = socket.recv().decode()
    print("RESPONSE:", response, "\n")
    return response

# Message Contract - Ping Request:
call({ "action": "ping" })
time.sleep(.2)

# Message Contract - Timestamp Request
call({ "action": "timestamp", "clientID": "TaskTracker", "eventName": "add.task" })
time.sleep(.2)

call({ "action": "timestamp", "clientID": "FitnessApp", "eventName": "add.workout" })
time.sleep(.2)

call({ "action": "timestamp", "clientID": "HabitTracker", "eventName": "add.habit" })
time.sleep(.2)

call({ "action": "timestamp", "clientID": "random", "eventName": "add.habit" })
time.sleep(.2)

# End server
socket.send_string("Q")  # (Q)uit will ask server to stop.

reply = socket.recv().decode()

try:
    data = json.loads(reply)
    print("EVENT LOG:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    pass

socket.close()
context.term()
