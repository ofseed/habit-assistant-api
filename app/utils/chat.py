import os

import openai
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion(prompt: str, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message["content"]
