import requests as req
import glob

import plotly.express as px
import pandas as pd

API_URL = 'https://api.languagetool.org/v2/check'
INPUT_DIR = 'input'

def check_grammar(file_path):
    with open(file_path, 'r') as file:
        res = req.post(API_URL, {
            'text': file.read(),
            'language': 'en-US',
        }).json()
    return len(res['matches'])

if __name__ == '__main__':
    for file_path in glob.glob(f'{INPUT_DIR}/*.txt'):
        print(f'Evaluating {file_path}...')
        print(f'Number of grammatical errors: {check_grammar(file_path)}')