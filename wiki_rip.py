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

def preprocess(text):
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
    text = re.sub(r'<ref.*>.*</ref>', '', text)
    text = re.sub(r'<sub>|<sub/>', '', text, count=0)
    text = re.sub(r'<!--.*-->', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'refn\|.*\|.*\|', ' ', text)
    if re.search(r'</ref>|-->', text):
        preprocess.is_multi_line = False
        text = re.sub(r'.*</ref>|-->', '', text)
    if preprocess.is_multi: text = ''
    if re.search(r'<ref>|<!--', text):
        preprocess.is_multi_line = True
        text = re.sub(r'(<ref>|<!--).*', '', text)
    return text.strip()
preprocess.is_multi_line = False

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
        if is_plot: plot.append(preprocess(line))
    return plot

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
        for paragraph in plot:
            if paragraph: file.write(f'{paragraph}\n\n')

def json_to_string(data):
    return json.dumps(data, indent=4, separators=(', ', ' = '))

def open_file():
    open(OUTPUT_PATH, 'w').close()
    return open(OUTPUT_PATH, 'a')

if __name__ == '__main__':
    global file
    file = open_file()
    expand_category(get_film_list())
    file.close()