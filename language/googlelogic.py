from google.cloud import language_v1
import os

def check_sentence_logic(sentence):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./json/naturallanguageprocessproject-55a163568b7d.json"

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=sentence, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(request={'document': document})

    tokens = response.tokens
    is_logical = not any(token.dependency_edge.head_token_index == token.dependency_edge.label for token in tokens)

    return is_logical

# Example usage
sentence = "I am am"
is_logical = check_sentence_logic(sentence)
print(f"The sentence '{sentence}' is logical: {is_logical}")
