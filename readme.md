**Calendar Microservice 3**

Returns a server-generated timestamp for events using ZeroMQ.

Features:
*** ping** -- see server status with a ping command
*** timestamp** -- returns a timestamp on event
*** event tracking** - tracks requests made by whitelisted apps


**Message Contract"**
PING
Request:
{ "action": "ping" }

Response:
{ "status": 200, "message": "pong" }


Timestamp
Request:
{
  "action": "timestamp",
  "clientID": "TaskTracker",
  "eventName": "add.task"
}


Response:
{
  "status": 200,
  "message": "timestamp",
  "timestamp": "2025-11-11T19:04:12Z"
}


Note: update or change your app name in the server.py whitelist -- and have that name refelcted in your calls.
