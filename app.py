import streamlit
import streamlit_option_menu
import query_chatgpt
import re
import set_env_variables
import retrieval

config = set_env_variables.set_env_variables_from_yaml("config.yaml")
config = config["twelvelabs"]

streamlit.set_page_config(
    layout="wide",
    page_title="Fix My Car",
    initial_sidebar_state="auto",
)

streamlit.title("NEL Visualization for NLP Engine")


def parse_statements(text):
    # Regular expression to match numerical indexes followed by statements
    pattern = r"\d+\.\s(.*?)(?=\d+\.\s|$)"

    # Extracting the statements
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of statements
    return [match.strip() for match in matches]


def get_video_index(steps, user_query):
    for i, step in enumerate(steps):
        query_prompt = f"for the query {user_query}, step {str(i) is step}"
        retrieval.query_marengo_in_twelvelabs(config=config, query_prompt=query_prompt)


def solve_user_query(user_query) -> None:
    chatoutput = query_chatgpt.query_chatgpt(user_query)
    print(chatoutput)

    steps = parse_statements(text=chatoutput)

    print(steps)


with streamlit.form(key="submit_query"):
    user_query = streamlit.text_input("How Can I Help?")
    submit_button = streamlit.form_submit_button(label="Submit")
    streamlit.write(user_query)
    # streamlit.text_area("How can I Help ?", key="user_query")
    # submit = streamlit.form_submit_button("Submit", on_click="solve_user_query")
    solve_user_query(user_query)
