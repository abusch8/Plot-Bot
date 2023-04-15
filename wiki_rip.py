import requests
import json

def get_film_list():
    api_url = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:American_science_fiction_films&cmlimit=500&format=json'
    return requests.get(api_url).json()['query']['categorymembers']

def get_film_page(id):
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&pageids={id}&prop=info&inprop=url&format=json'
    return requests.get(api_url).json()

def json_to_string(data):
    return json.dumps(data, indent=4, separators=(', ', ' = '))

if __name__ == '__main__':
    film_list = get_film_list()
    print(json_to_string(film_list))
    film = get_film_page(film_list[0]['pageid'])
    print(json_to_string(film))