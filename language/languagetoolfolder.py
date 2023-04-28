import requests
import os

def fix_grammar(folder_path):
    url = 'https://api.languagetool.org/v2/check'
    file_paths = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_paths.append(os.path.join(folder_path, file_name))

    print(file_paths);
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            text = file.read() 
      
        payload = {
        'text': text,
        'language': 'en-US',
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        corrections = data['matches']
        num_corrections = len(corrections)

        # Correct grammar and return the fixed text
        fixed_text = text
        for correction in corrections:
            offset = correction['offset']
            length = correction['length']
            replacement = correction['replacements'][0]['value']
            fixed_text = fixed_text[:offset] + replacement + fixed_text[offset + length:]

            print("File path:", file_path)
            print()
            print("Fixed text:", fixed_text)
            print("Number of grammar corrections:", num_corrections)
            print()
            break;
        else:
            # Handle API error
            print(f"LanguageTool API request failed with status code {response.status_code}")
            return

# Example usage
folder_path = './textFolder/'
fix_grammar(folder_path)
