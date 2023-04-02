import requests
import json

search_term = input("Search: ")

api_url = 'https://imdb-api.com/en/API/SearchMovie/k_k1c2il8w/{}'.format(search_term)
response = requests.get(api_url)
results = response.json()["results"]
for x in range(len(results)):
    print("{}) {}".format(x + 1, results[x]["title"]))
index = int(input("Select a result: ")) - 1

api_url = 'https://imdb-api.com/en/API/Title/k_k1c2il8w/{}'.format(results[index]["id"])
response = requests.get(api_url)
results = json.dumps(response.json(), indent=4, separators=(", ", " = "))
print(results)