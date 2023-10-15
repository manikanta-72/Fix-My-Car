import requests
import glob
from pprint import pprint
import os

import time

# Retrieve the URL of the API and my API key
API_URL = os.getenv("API_URL")
assert API_URL

API_KEY = os.getenv("API_KEY")
assert API_KEY

# Construct the URL of the `/indexes` endpoint
INDEXES_URL = f"{API_URL}/indexes"

# Specify the name of the index
INDEX_NAME = "Content Creator Videos"

# Set the header of the request
headers = {"x-api-key": API_KEY}

# Declare the /tasks/external-provider endpoint
TASKS_URL = f"{API_URL}/tasks/external-provider"

# Construct the body of the request
data = {
    "index_id": INDEX_ID,  # Specify the unique ID of the index
    "url": "https://youtu.be/0Hc0Z6zFbzM?si=a1oqVb0Eve9yzxMD",  # Specify the YouTube URL of the video
}

# Upload the video
response = requests.post(TASKS_URL, headers=headers, json=data)

# Store the ID of the task in a variable named TASK_ID
TASK_ID = response.json().get("_id")

# Print the status code and response
print(f"Status code: {response.status_code}")
pprint(response.json())


# Define starting time
start = time.time()
print("Start uploading video")

# Monitor the indexing process
TASK_STATUS_URL = f"{API_URL}/tasks/{TASK_ID}"
while True:
    response = requests.get(TASK_STATUS_URL, headers=headers)
    STATUS = response.json().get("status")
    if STATUS == "ready":
        print(f"Status code: {STATUS}")
        break
    time.sleep(10)

# Define ending time
end = time.time()
print("Finish uploading video")
print("Time elapsed (in seconds): ", end - start)

# Retrieve the unique identifier of the video
VIDEO_ID = response.json().get("video_id")

# Print the status code, the unique identifier of the video, and the response
print(f"VIDEO ID: {VIDEO_ID}")
pprint(response.json())
