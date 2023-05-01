import spacy

def check_sentence_logic(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    # Check for duplicate words
    is_logic_correct = not any([token.text == token.head.text for token in doc])

    return is_logic_correct

# Example usage
sentence = "I am am"
is_logical = check_sentence_logic(sentence)
print(f"The sentence '{sentence}' is logical: {is_logical}")
