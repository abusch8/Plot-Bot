import requests
import json
import io

def get_film_list():
    api_url = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:American_science_fiction_films&cmlimit=500&format=json'
    return requests.get(api_url).json()['query']['categorymembers']

def get_film_page(id):
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&pageids={id}&prop=revisions&rvprop=content&format=json'
    page = requests.get(api_url).json()
    return page['query']['pages'][str(id)]['revisions'][0]['*']

def clear_file(path): open(path, 'w').close()

def write_file(path, line):
    file = open(path, 'a')
    file.write(line)
    file.close()

def json_to_string(data):
    return json.dumps(data, indent=4, separators=(', ', ' = '))

if __name__ == '__main__':
    path = 'output.txt'
    clear_file(path)

    film_list = get_film_list()
    print(json_to_string(film_list))

    for x in range(10):
        page_id = film_list[x]['pageid']
        film_page = get_film_page(page_id)

        lines = film_page.splitlines()
        for line in lines:
            print(line)
            write_file(path, f'{line}\n')
