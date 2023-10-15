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

# Set the header of the request
headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

# List indexes
url = f"{API_URL}/indexes?page=1&page_limit=10&sort_by=created_at&sort_option=asc"

response = requests.get(url, headers=headers)
print(f"Status code: {response.status_code}")
pprint(response.json())
