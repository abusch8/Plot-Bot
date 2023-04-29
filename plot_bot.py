import os
import requests
import json
import openai
from dotenv import load_dotenv

def search_api(term):
    api_url = f'https://imdb-api.com/en/API/SearchMovie/k_k1c2il8w/{term}'
    response = requests.get(api_url)
    result = response.json()['results']
    return result

def get_movie_info(id):
    api_url = f'https://imdb-api.com/en/API/Title/k_k1c2il8w/{id}'
    return requests.get(api_url).json()

def json_to_string(data):
    return json.dumps(data, indent=4, separators=(', ', ' = '))

def generate_prompt(movie_data):
    return f'Write a movie synopsis that combines the following movie plots:\n{movie_data[0]["plot"]}\n{movie_data[1]["plot"]}\n{movie_data[2]["plot"]}\n'

def generate_response(prompt):
    model_engine = 'text-davinci-003'
    prompt = (f'{prompt}')
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

if __name__ == '__main__':
    load_dotenv('.env.local')
    openai.api_key = os.getenv('API_KEY')

    movie_info = []
    for x in range(3):
        search_term = input('Search: ')

        result = search_api(search_term)
        for y in range(len(result)):
            print(f'{y + 1}) {result[y]["title"]}')
        index = int(input('Select a result: ')) - 1

        movie_info.append(get_movie_info(result[index]['id']))
        print(f'####\n{movie_info[x]["title"].upper()}\n####\n{json_to_string(movie_info[x])}\n')

    prompt = generate_prompt(movie_info);
    response = generate_response(prompt);
    print(response)