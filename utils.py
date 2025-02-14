from openai import OpenAI
from dotenv import load_dotenv
import os
import keyring
import getpass 

# Initialize the OpenAI client
dotenv_path = os.path.join(os.path.dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
open_ai_key = os.getenv('OPENAI_API_KEY') 
client = OpenAI(api_key=open_ai_key)

def get_llm_analysis(content, system_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content}
    ]

    # Call the chat completions endpoint
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Return the response message
    return completion.choices[0].message.content


def setup_credentials():
    username = input("Enter your LinkedIn username: ")
    password = getpass.getpass("Enter your LinkedIn password: ")  # Password input will be hidden
    keyring.set_password("linkedin", "username", username)
    keyring.set_password("linkedin", username, password)
    print("Credentials stored securely in system keyring")
