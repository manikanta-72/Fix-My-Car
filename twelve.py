from typing import Dict, Any
import requests
import glob
from pprint import pprint
import os
import pandas
import set_env_variables
import time
import csv


def get_config(config_path: str) -> Dict[str, Any]:
    return set_env_variables.set_env_variables_from_yaml(config_path)


def create_index_in_twelvelabs(config: Dict[str, Any]):
    print("config: ", config)
    headers = {"x-api-key": config["api_credentials"]["api_key"]}

    # Declare a dictionary named data
    data = {
        "engines": [
            {
                "engine_name": "marengo2.5",  # Configure the video understanding engine
                "engine_options": [
                    "visual",
                    "conversation",
                    "text_in_video",
                    "logo",
                ],  # Specify the engine options
            },
            {
                "engine_name": "pegasus1",  # Configure the video understanding engine
                "engine_options": [
                    "visual",
                    "conversation",
                ],  # Specify the engine options
            },
        ],
        "index_name": config["index"]["name"],
        "addons": ["thumbnail"],  # Enable the thumbnail generation feature
    }

    # Create an index
    response = requests.post(config["index"]["url"], headers=headers, json=data)

    print(f"Status code: {response.status_code}")

    pprint(response.json())


def create_marengo_index_in_twelvelabs(config: Dict[str, Any]):
    print("config: ", config)
    headers = {"x-api-key": config["api_credentials"]["api_key"]}

    # Declare a dictionary named data
    data = {
        "engines": [
            {
                "engine_name": "marengo2.5",  # Configure the video understanding engine
                "engine_options": [
                    "visual",
                    "conversation",
                    "text_in_video",
                    "logo",
                ],  # Specify the engine options
            },
        ],
        "index_name": config["marengo_index"]["name"],
        "addons": ["thumbnail"],  # Enable the thumbnail generation feature
    }

    # Create an index
    response = requests.post(config["marengo_index"]["url"], headers=headers, json=data)

    print(f"Status code: {response.status_code}")

    print(response.json())
    # Store the unique identifier of your index
    INDEX_ID = response.json().get("_id")

    return INDEX_ID


def upload_video_to_index(config: str, video_url: str) -> None:
    # do nothing
    # Set the header of the request
    headers = {"x-api-key": config["api_credentials"]["api_key"]}

    task_url = config["api_credentials"]["task_url"]

    print("index_id: ", config["marengo_index"]["id"])
    print(f"task_url: ", task_url)
    # Construct the body of the request
    data = {
        "index_id": config["marengo_index"]["id"],  # Specify the unique ID of the index
        "url": video_url,  # Specify the YouTube URL of the video
    }

    # Upload the video
    response = requests.post(task_url, headers=headers, json=data)

    # Store the ID of the task in a variable named TASK_ID
    task_id = response.json().get("_id")
    print(f"task response: ", response.json())

    # Define starting time
    start = time.time()
    print("Start uploading video")

    api_url = config["api_credentials"]["api_url"]
    # Monitor the indexing process
    TASK_STATUS_URL = f"{api_url}/tasks/{task_id}"
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
    video_id = response.json().get("video_id")

    return video_id


def load_videos_to_indexes(config: str) -> None:
    df = pandas.read_csv(config["marengo_index"]["url_data_file"])
    video_ids = []
    for i, row in df.iterrows():
        if i > 29:
            print(f"*********{i}**********")
            video_id = upload_video_to_index(config=config, video_url=row["url"])
            print(video_id)
            video_ids.append(video_id)
    df["video_id"] = video_ids

    df.to_csv("yt_car_self_help_with_ids_1.csv", index=False)


def list_indexes(config):
    # Set the header of the request
    headers = {
        "x-api-key": config["api_credentials"]["api_key"],
        "Content-Type": "application/json",
    }

    api_url = config["api_credentials"]["api_url"]
    # List indexes
    url = f"{api_url}/indexes?page=1&page_limit=10&sort_by=created_at&sort_option=asc"

    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    pprint(response.json())


def query_video_metadata(config, video_id):
    headers = {
        "accept": "application/json",
        "x-api-key": config["api_credentials"]["api_key"],
        "Content-Type": "application/json",
    }

    index_id = config["marengo_index"]["id"]
    query_url = f"https://api.twelvelabs.io/v1.1/indexes/{index_id}/videos/{video_id}"

    response = requests.get(query_url, headers=headers)

    response_json = response.json()

    source_url = response_json["source"]["url"]

    print(source_url)
    return source_url


def list_videos_in_marengo_index(config):
    # Set the header of the request
    headers = {
        "x-api-key": config["api_credentials"]["api_key"],
        "Content-Type": "application/json",
    }

    index_id, api_url = (
        config["marengo_index"]["id"],
        config["api_credentials"]["api_url"],
    )
    # List all the videos in an index
    # url = "https://api.twelvelabs.io/v1.1/indexes/652b45e93c4a426cf3f4f96b/videos?page=1&page_limit=50&sort_by=created_at&sort_option=desc"

    INDEXES_VIDEOS_URL = f"{api_url}/indexes/{index_id}/videos?page=1&page_limit=50&sort_by=created_at&sort_option=desc"
    response = requests.get(INDEXES_VIDEOS_URL, headers=headers)
    print(f"Status code: {response.status_code}")
    pprint(response.json())
    data = response.json()["data"]
    print(f"data: {data}")
    print(type(data))
    print(len(data))
    video_dictionary = {"video_id": [], "source_url": []}
    for video in data:
        video_id = video["_id"]
        source_url = query_video_metadata(config, video_id=video_id)
        video_dictionary["video_id"].append(video_id)
        video_dictionary["source_url"].append(source_url)
    # Get the headers (column names) from the dictionary keys
    headers = list(video_dictionary.keys())
    # Create or overwrite the CSV file
    with open("id_url.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write the headers first
        writer.writerow(headers)

        # Zip the values from the dictionary together and write each row
        for row in zip(*video_dictionary.values()):
            writer.writerow(row)


def init_twelve(config_file: str) -> None:
    config = get_config(config_path=config_file)

    # create index of car files in twelvelabs
    # create_index_in_twelvelabs(config=config["twelvelabs"])
    # create_marengo_index_in_twelvelabs(config=config["twelvelabs"])

    # load data to indexes
    # load_videos_to_indexes(config=config["twelvelabs"])

    # list_indexes(config["twelvelabs"])

    list_videos_in_marengo_index(config=config["twelvelabs"])


if __name__ == "__main__":
    init_twelve(config_file="config.yaml")
