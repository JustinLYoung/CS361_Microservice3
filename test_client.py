# microservice test client 

import json
import zmq

context = zmq.Context()
print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Sending a request...")


# call function -- what we use to communicate to server
def call(object):
    socket.send_string(json.dumps(object))
    print("REQEST :", object)
    # Message Contract -- Server Reply:
    response = socket.recv().decode()
    print("RESPONSE:", response, "\n")
    return response

# Message Contract - Ping Request:
call({ "action": "ping" })

# Message Contract - Timestamp Request
call({ "action": "timestamp", "clientID": "TaskTracker", "eventName": "add.task" })


# End server
socket.send_string("Q")  # (Q)uit will ask server to stop.
# close and terminate test program
socket.close()
socket.term()
