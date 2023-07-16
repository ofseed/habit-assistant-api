import os

import openai
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion(prompt: str, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": f"""
            你是一个习惯管理助手，用户告诉你一个精确的时间他在做些什么，你给用户一些建议, 
            包含对用户生活习惯的建议，这个对应的时间段应该怎样使用手机，字数不大于100字。
            """,
        },
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
