
import os
import config
from groq import Groq

groq_api_key = config.GROQ_API_KEY
client = Groq(api_key=groq_api_key)

def create_llm_answer(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content