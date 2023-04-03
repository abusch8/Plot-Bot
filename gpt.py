import os
import openai
from dotenv import load_dotenv

load_dotenv(".env.local")
openai.api_key = os.getenv("API_URL")

def generate_response(prompt):
    model_engine = "text-davinci-003"
    prompt = (f"{prompt}")
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message.strip()

if __name__ == "__main__":
    prompt = input("Prompt: ")
    print(generate_response(prompt))