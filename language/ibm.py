import requests
import json

def analyze_sentence(sentence):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/{YOUR_INSTANCE_ID}/v1/analyze"
    api_key = "YOUR_API_KEY"

    params = {
        "version": "2021-03-25",
        "features": "sentiment",
        "text": sentence
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=("apikey", api_key), params=params, headers=headers)
    response_json = response.json()

    sentiment = response_json["sentiment"]["document"]["label"]
    return sentiment

# Example usage
sentence = "I am happy"
sentiment = analyze_sentence(sentence)
print(f"The sentiment of the sentence '{sentence}' is: {sentiment}")
