import requests
import os

API_URL = 'https://api.languagetool.org/v2/check'
INPUT_DIR = 'input'

def fix_grammar(input_dir):
    file_paths = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            file_paths.append(os.path.join(input_dir, file_name))

    print(file_paths);
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            print("Evaluating ", file_path)
            text = file.read()
            res = requests.post(API_URL, data={
                'text': text,
                'language': 'en-US',
            }).json()
            print("Number of grammatical errors: ", len(res['matches']))

if __name__ == '__main__':
    fix_grammar(INPUT_DIR)
