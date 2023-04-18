import requests as req
import json
import re

API_URL = 'https://en.wikipedia.org/w/api.php'
GENRE = 'American_science_fiction_films'
OUTPUT_PATH = f'data/{GENRE}.txt'

memory = []

def get_film_list(id=None):
    res = req.get(API_URL, {
        'action': 'query',
        'list': 'categorymembers',
        **({'cmtitle': f'Category:{GENRE}'} if id is None else {'cmpageid': id}),
        'cmlimit': 500,
        'format': 'json'
    }).json()
    return res['query']['categorymembers']

def get_film_page(id):
    res = req.get(API_URL, {
        'action': 'parse',
        'pageid': id,
        'prop': 'wikitext',
        'format': 'json'
    }).json()
    return res['parse']['wikitext']['*']

def preprocess_data(text): #TODO: Handle multi line HTML elements
    text = re.sub(r'\[\[(File|Image):.*\]\]', '', text)
    for match in re.findall(r'\[\[[^\[\]\|]*\|[^\[\]]*\]\]', text):
        text = text.replace(match, match.split('|')[1][:-2])
    text = re.sub(r'^\{\{.*\|.*\}\}$', '', text)
    text = re.sub(r'\[\[|\]\]', '', text, count=0)
    text = re.sub(r'\{\{-\}\}', '', text)
    text = re.sub(r'\{\{|\}\}', '', text, count=0)
    text = re.sub(r'\'\'', '\"', text)
    text = re.sub(r'"\[https://.*\]"', '', text)
    text = re.sub(r'\[http://.*\]', '', text)
    text = re.sub(r'<ref.*/>', '', text)
    text = re.sub(r'<ref.*>*</ref>', '', text)
    text = re.sub(r'<!--.*-->', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'refn\|.*\|.*\|', ' ', text)
    return text.strip()

def parse_plot(page):
    plot = []
    is_plot = False
    for line in page.splitlines():
        if line == '==Plot==':
            is_plot = True
            continue
        elif re.match(r'^.*==.*==.*$', line):
            is_plot = False
            break
        if is_plot: plot.append(preprocess_data(line))
    return plot

def json_to_string(data):
    return json.dumps(data, indent=4, separators=(', ', ' = '))

def expand_category(category):
    print('####\nEXPANDING CATEGORY\n####')
    print(json_to_string(category))
    for page in category:
        title, pageid = page['title'], page['pageid']
        if pageid in memory: continue
        memory.append(pageid)
        if re.match(r'^File:.*$', title): continue
        if re.match(r'^Category:.*$', title):
            expand_category(get_film_list(pageid))
            continue
        plot = parse_plot(get_film_page(pageid))
        print(f'Writing \033[1m\33[3m{title}\033[0m \033[96m[ID:{pageid}]\033[0m to {OUTPUT_PATH}')
        if plot: file.write(f'####{title}####\n')
        for line in plot: file.write(f'{line}\n')

def open_file():
    open(OUTPUT_PATH, 'w').close() # Clear file
    return open(OUTPUT_PATH, 'a')

if __name__ == '__main__':
    global file
    file = open_file()
    expand_category(get_film_list())
    file.close()