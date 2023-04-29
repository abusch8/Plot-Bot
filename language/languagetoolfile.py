import requests

def fix_grammar(file_path):
    url = 'https://api.languagetool.org/v2/check'
  
    with open(file_path, 'r') as file:
        text = file.read();
   
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

        return fixed_text, num_corrections
    else:
        # Handle API error
        print(f"LanguageTool API request failed with status code {response.status_code}")
        return text, 0

# Example usage
file_path = 'file.txt'
fixed_text, num_corrections = fix_grammar(file_path)
print("File path:", file_path)
print()
print("Fixed text:", fixed_text)
print("Number of grammar corrections:", num_corrections)
