import requests
import json

search_term = input('Search: ')

api_url = f'https://imdb-api.com/en/API/SearchMovie/k_k1c2il8w/{search_term}'
response = requests.get(api_url)
result = response.json()['results']
for x in range(len(result)):
    print(f'{x + 1}) {result[x]["title"]}')
index = int(input('Select a result: ')) - 1

api_url = f'https://imdb-api.com/en/API/Title/k_k1c2il8w/{result[index]["id"]}'
response = requests.get(api_url)
result = json.dumps(response.json(), indent=4, separators=(', ', ' = '))
print(result)