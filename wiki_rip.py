import requests
import json
import re

def get_film_list(category):
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&cmlimit=500&format=json'
    res = requests.get(api_url).json()
    return res['query']['categorymembers']

def get_film_page(id):
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&pageids={id}&prop=revisions&rvprop=content&format=json'
    res = requests.get(api_url).json()
    return res['query']['pages'][str(id)]['revisions'][0]['*']

def parse_plot(page):
    plot = []
    lines = page.splitlines()
    is_plot = False
    for line in lines:
        if line == '==Plot==': is_plot = True
        elif re.match(r'^==.*==$', line): is_plot = False
        if is_plot: plot.append(line)
    return plot

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

    film_list = get_film_list('American_science_fiction_films')
    print(json_to_string(film_list))

    for x in range(10):
        film_page = get_film_page(film_list[x]['pageid'])
        plot = parse_plot(film_page)
        print('Writing file...')
        for line in plot: write_file(path, f'{line}\n')
