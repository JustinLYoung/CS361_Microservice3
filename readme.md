# Calendar Microservice 3 
Returns a server-generated timestamp for events using ZeroMQ. No database; events are stored in memory during runtime and written as a JSON file on shutdown.

## Features:
* ping -- see server status with a ping command
* timestamp -- returns a timestamp on event
* event tracking - tracks requests made by whitelisted apps

## Requirements:
* Python
* json
* pyzmq

## Running the Server:
1. How to start:
Download the python file and run the server in your terminal, you should see the following:
```
server.py
# [microservice3 3] listening on tcp:///*:5555
```
2. How to stop:
* stop the servia via command line comand <kbd>Ctrl</kbd>+<kbd>C</kbd> or by sending <kbd>Q </kbd> message in client. (See test client)
  
## Message Contract
* Protocol: ZeroMQ
* Pattern: REQ/REP
* Sever: `tcp://*:5555`
* Encoding: JSON (UTF-8)

### 1. PING
Request:
`{ "action": "ping" } `

Response:
`{ "status": 200, "message": "pong" }`


### 2. Timestamp
Request:
```
{
  "action": "timestamp",
  "clientID": "TaskTracker",
  "eventName": "add.task"
}
```

Response:
```
{
  "status": 200,
  "message": "timestamp",
  "timestamp": "2025-11-11T19:04:12Z"
}
```
Note: 
update or change your app name in the server.py whitelist -- and have that name refelcted in your calls.

## How to <ins>Request</ins> Data programatically
Install all dependencies and set up the ZMQ socket.
Use the `call()` function below to send a request to the server.
```
import json
import zmq

context = zmq.Context()
print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Sending a request...")
# call function 
def call(object):
    socket.send_string(json.dumps(object))
    print("REQEST :", object)
    # Message Contract -- Server Reply:
    response = socket.recv().decode()
    print("RESPONSE:", response, "\n")
    return response
```
Example call:
`call({ "action": "ping" })`

## How to <ins>Receive</ins> Data programatically
Receiving is performed inside the `call()` function. The function will make a call to the server, return a JSON reply, decode it, and print that response in the program terminal.
```
def call(object):
    socket.send_string(json.dumps(object))
    print("REQEST :", object)
    # Message Contract -- Server Reply:
    response = socket.recv().decode()
    print("RESPONSE:", response, "\n")
    return response
```
Example call:
`{ "status": 400, "error": "invalid json" }`

## UML diagram
[in progress -- EOD today]
