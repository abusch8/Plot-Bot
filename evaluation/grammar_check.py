import requests as req
import glob

import plotly.express as px
import pandas as pd

API_URL = 'https://api.languagetool.org/v2/check'
DATA_DIR = '../nanoGPT/out-fantasy'

def check_grammar(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        res = req.post(API_URL, {
            'text': file.read(),
            'language': 'en-US',
        }).json()
    return len(res['matches'])

def plot(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='iter', y='errors', title='Grammatical Errors Over Iterations')
    fig.show()

if __name__ == '__main__':
    data = { 'iter': [], 'errors': [] }
    extract_number = lambda s: int(''.join(filter(str.isdigit, s)))
    for file_path in sorted(glob.glob(f'{DATA_DIR}/*.txt'), key=extract_number):
        print(f'Evaluating {file_path}...')
        errors = check_grammar(file_path)
        print(f'Number of grammatical errors: {errors}')
        data['iter'].append(extract_number(file_path))
        data['errors'].append(errors)
    print('Plotting results...')
    plot(data)
