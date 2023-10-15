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

# Construct the URL of the `/search` endpoint
SEARCH_URL = f"{API_URL}/search/"

# Set the header of the request
headers = {"x-api-key": API_KEY}

query = "A woman wearing makeup"

# Declare a dictionary named `data`
data = {
    "query": query,  # Specify your search query
    "index_id": INDEX_ID,  # Indicate the unique identifier of your index
    "search_options": ["visual"],  # Specify the search options
}

# Make a search request
response = requests.post(SEARCH_URL, headers=headers, json=data)
print(f"Status code: {response.status_code}")
pprint(response.json())
