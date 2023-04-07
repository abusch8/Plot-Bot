import requests
import json

def search_api(term):
    api_url = f'https://imdb-api.com/en/API/SearchMovie/k_k1c2il8w/{term}'
    response = requests.get(api_url)
    result = response.json()['results']
    return result

def get_movie_info(id):
    api_url = f'https://imdb-api.com/en/API/Title/k_k1c2il8w/{id}'
    response = requests.get(api_url)
    result = json.dumps(response.json(), indent=4, separators=(', ', ' = '))
    return result

if __name__ == '__main__':
    selections = []
    for x in range(3):
        search_term = input('Search: ')

        result = search_api(search_term)
        for x in range(len(result)):
            print(f'{x + 1}) {result[x]["title"]}')
        index = int(input('Select a result: ')) - 1

        selections.append(result[index])

    for movie in selections:
        print(f'####\n{movie["title"].upper()}\n####\n', get_movie_info(movie["id"]))