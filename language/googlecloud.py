from google.cloud import language_v1
import os

def analyze_sentence(sentence):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./json/naturallanguageprocessproject-55a163568b7d.json"

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=sentence, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})

    sentiment = response.document_sentiment.score
    return sentiment

# Example usage
sentence = "I am happy"
sentiment = analyze_sentence(sentence)
print(f"The sentiment of the sentence '{sentence}' is: {sentiment}")
