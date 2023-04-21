import requests as req
import json
import re

API_URL = 'https://en.wikipedia.org/w/api.php'

memory = []

def get_category(id=None, genre=None):
    if not id and not genre: SystemExit('')
    try:
        res = req.get(API_URL, {
            'action': 'query',
            'list': 'categorymembers',
            **({'cmtitle': f'Category:{genre}'} if genre else {}),
            **({'cmpageid': id} if id else {}),
            'cmlimit': 500,
            'format': 'json'
        })
        print(res.json())
        res.raise_for_status()
    except req.exceptions.RequestException as err: SystemExit(err)
    return res.json()['query']['categorymembers']

def get_film_page(id):
    try:
        res = req.get(API_URL, {
            'action': 'parse',
            'pageid': id,
            'prop': 'wikitext',
            'format': 'json'
        })
        res.raise_for_status()
    except req.exceptions.RequestException as err: SystemExit(err)
    return res.json()['parse']['wikitext']['*']

def preprocess(text):
    text = re.sub(r'\[\[(File|Image):.*\]\]', '', text)
    for match in re.findall(r'\[\[[^\[\]\|]*\|[^\[\]]*\]\]', text):
        text = text.replace(match, match.split('|')[1][:-2])
    text = re.sub(r'^\{\{.*\|.*\}\}$', '', text)
    text = re.sub(r'\[\[|\]\]', '', text, count=0)
    text = re.sub(r'\{\{-\}\}', '', text)
    text = re.sub(r'\{\{|\}\}', '', text, count=0)
    text = re.sub(r'\'\'', '\"', text)
    text = re.sub(r'^:\"Note:.*\"$', '', text)
    text = re.sub(r'\[http(|s)://.*\]', '', text)
    text = re.sub(r'\"\"', '', text)
    text = re.sub(r'<ref.*/>', '', text)
    text = re.sub(r'<ref.*>.*</ref>', '', text)
    text = re.sub(r'<sub>|<sub/>', '', text, count=0)
    text = re.sub(r'<!--.*-->', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'refn\|.*\|.*\|', ' ', text)
    if re.search(r'</ref>|-->', text):
        preprocess.is_multi_line = False
        text = re.sub(r'.*</ref>|-->', '', text)
    if preprocess.is_multi_line: text = ''
    if re.search(r'<ref>|<!--', text):
        preprocess.is_multi_line = True
        text = re.sub(r'(<ref>|<!--).*', '', text)
    return text.strip()
preprocess.is_multi_line = False

def parse_plot(page):
    plot = ''
    is_plot = False
    for line in page.splitlines():
        if line == '==Plot==': is_plot = True
        elif re.match(r'^.*==.*==.*$', line): is_plot = False
        elif is_plot: plot += f'{preprocess(line)}\n'
    return plot.strip()

def json_to_string(data):
    return json.dumps(data, indent=4, separators=(', ', ' = '))

def expand_category(category):
    print('\033[1m\033[3m####\nEXPANDING CATEGORY\n####\033[0m')
    print(json_to_string(category))
    for page in category:
        title = re.sub(r'\ \(.*film\)', '', page['title'])
        page_id = page['pageid']
        if page_id in memory:
            print(f'\033[91mSKIPPED\033[0m \033[1m\033[3m{title}\033[0m \033[96m[ID:{page_id}]\033[0m Reason: Duplicate')
            continue
        memory.append(page_id)
        if re.match(r'^File:.*$', title): continue
        if re.match(r'^Category:.*$', title):
            expand_category(get_category(page_id))
            continue
        plot = parse_plot(get_film_page(page_id))
        if plot:
            print(f'\033[92mWRITING\033[0m \033[1m\033[3m{title}\033[0m \033[96m[ID:{page_id}]\033[0m Output: {output_path}')
            file.write(f'####{title}####\n{plot}\n\n')
        else:
            print(f'\033[91mSKIPPED\033[0m \033[1m\033[3m{title}\033[0m \033[96m[ID:{page_id}]\033[0m Reason: No plot')

def get_genre_options():
    options = []
    genre_list = get_category(genre='American_films_by_genre')
    for i in range(len(genre_list)):
        options.append(genre_list[i])
    return options

def open_file(path):
    open(path, mode='w').close()
    return open(path, mode='a', encoding="utf-8")

if __name__ == '__main__':
    global file
    global output_path
    options = get_genre_options()
    for i in range(len(options)):
        title = re.sub(r'Category:', '', options[i]["title"])
        print(f'{i + 1}) {title}')
    choice = int(input('Genre: ')) - 1
    title = re.sub(r'Category:', '', options[choice]["title"])
    output_path = f'data/{title}.txt'
    file = open_file(output_path)
    if choice not in range(len(options)): SystemExit('')
    expand_category(get_category(options[choice]['pageid']))
    file.close()
    print('\033[1m\33[3m####\nCOMPLETED\n####\033[0m')