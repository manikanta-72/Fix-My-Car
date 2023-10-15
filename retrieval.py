import requests
import pprint
import set_env_variables


def query_marengo_in_twelvelabs(config: str, query_prompt: str):
    headers = {"x-api-key": config["api_credentials"]["api_key"]}

    # Declare a dictionary named `data`
    data = {
        "query": query_prompt,  # Specify your search query
        "index_id": config["marengo_index"][
            "id"
        ],  # Indicate the unique identifier of your index
        "search_options": ["visual"],  # Specify the search options
    }

    # Make a search request
    response = requests.post(
        config["api_credentials"]["search_url"], headers=headers, json=data
    )
    print(f"Status code: {response.status_code}")
    print(response.json())
    json_data = response.json()["data"]


def main(config: str):
    query = "How to change the engine oil ?"

    query_marengo_in_twelvelabs(config=config, query_prompt=query)


if __name__ == "__main__":
    config = set_env_variables.set_env_variables_from_yaml("config.yaml")
    main(config=config["twelvelabs"])
