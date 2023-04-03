import requests
import json

api_url = "https://imdb-api.com/en/API/Top250Movies/k_k1c2il8w"
response = requests.get(api_url)
print(json.dumps(response.json(), indent=4, separators=(", ", " = ")))