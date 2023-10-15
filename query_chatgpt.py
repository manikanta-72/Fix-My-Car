import set_env_variables
import openai


def query_chatgpt(query):
    url = "https://api.openai.com/v1/chat/completions"  # Note: this endpoint might change. Refer to the official OpenAI docs for the latest.

    # Your OpenAI API Key
    api_key = "YOUR_API_KEY_HERE"

    # Request headers
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    openai.api_key = "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"
    engine = "gpt-3.5-turbo"

    prompt_header = "Mention the major steps involved in answering the following question. The question is about fixing cars and answer it in 15 words.\n"
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[{"role": "user", "content": prompt_header + query}],
        max_tokens=50,
        # temperature = 0.5,
    )
    gpt_response = response.choices[0].message.content.strip()

    print(gpt_response)
    return gpt_response


if __name__ == "__main__":
    config = set_env_variables.set_env_variables_from_yaml("config.yaml")
