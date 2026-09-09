import requests
import json

data = {
    "problem": "my AC is broken",
    "location": "Columbus, OH",
    "preferred_date": "Tomorrow",
    "preferred_time": "Morning"
}

with requests.Session() as s:
    # First submit the request to set session
    s.post("http://127.0.0.1:5000/request", data=data)
    # Then hit process
    res = s.post("http://127.0.0.1:5000/api/process")
    print("Status:", res.status_code)
    print("Body:", res.text)
