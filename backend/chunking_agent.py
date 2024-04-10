from dotenv import load_dotenv
import os
import pandas as pd
from langchain.llms import OpenAI
import re


def get_secret(): 
    load_dotenv_success = load_dotenv()
    if load_dotenv_success:
        print("Environment variables loaded successfully.")
    else:
        print("Failed to load .env file.")
    openai_token = os.getenv('OPENAI_TOKEN')
    return(openai_token)


class ChatGPTApp:
    def __init__(self, api_key):
        self.llm = OpenAI(api_key=api_key)  
        self.system_message = None
        self.last_user_message = None

    def send_message(self, user_message):
        # Build the message with the system message and the last user message
        messages = []
        if self.system_message:
            messages.append(self.system_message)
        if self.last_user_message:
            messages.append(self.last_user_message)
        messages.append(user_message)
        full_message = ' '.join(messages)
        response = self.llm(full_message)
        # Update the last user message
        self.last_user_message = user_message
        return response
    
    def add_system_message(self, system_message):
        # Update the system message
        self.system_message = system_message


def process_script_in_chunks(title, script, chunk_size, overlap_size, max_iterations=50):
    responses = []
    start = 0
    end = chunk_size
    for _ in range(max_iterations):
        # Extract the chunk of text
        text_chunk = script[start:end]
        # Prepare and send the user message
        user_message = f"Process the following text from the movie {title}: {text_chunk}"
        response = app.send_message(user_message)
        responses.append(response)
        # Update the start and end for the next chunk
        start = end - overlap_size  # Overlap with the previous chunk
        end = start + chunk_size
        print(response)
        # Check if end exceeds script length
        if end > len(script):
            break
    return responses


def compile_responses_to_df(responses, title):
    # Pattern to extract table data
    table_pattern = re.compile(r"\|\s*(?P<title>.+?)\s*\|\s*(?P<description>.+?)\s*\|\s*(?P<text>.+?)\s*\|")
    # List to store each row as a dictionary
    rows = []
    for response in responses:
        matches = table_pattern.finditer(response)
        for match in matches:
            # Add each row to the rows list
            row = {
                'Title': title,
                'Line Description': match.group('description').strip(),
                'Line Text': match.group('text').strip()
            }
            rows.append(row)
    # Create DataFrame from the rows
    df = pd.DataFrame(rows, columns=['Title', 'Line Description', 'Line Text'])
    return df


# Usage


api_key = get_secret()
app = ChatGPTApp(api_key)
# Example of adding a system message
app.add_system_message("""
System: Your task is to analyze movie script lines, categorizing each line as either dialogue, scene description, direction/transition, technical notes or other. 
    For each line, you will create a table entry with the following columns: 'Title', 'Line Description', and 'Line Text'. The 'Line Description' 
    should specify the category of the line. Remember:

    1. Dialogue: Lines spoken by characters. Look for character names in CAPS followed by their spoken lines.
    2. Scene Description: Narrative text describing the setting or action, not spoken by characters.
    3. Direction/Transition: Technical instructions for the film, like camera angles or scene transitions (e.g., 'CUT TO:', 'INT.', 'EXT.').
    4. Technical Notes: Specific notes related to the production of the scene.
    5. Other: For anything that doesnt fit the first four categories. 

    Ensure each line is complete; partial lines at the beginning or end of the text should be ignored. Avoid duplicating lines from previous processing. 
    Present your analysis in a tabular (without the header) format for clarity using | to seperate the data (refer to previous message for consistency).
""")

first_script = scripts_df.iloc[0]['script']  # Retrieve the first script from the DataFrame
title = scripts_df.iloc[0]['title']
chunk_size = 500
overlap_size = 100

responses = process_script_in_chunks(title, first_script, chunk_size, overlap_size)
df = compile_responses_to_df(responses, title)