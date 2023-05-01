import pkgutil

def check_spacy_installed():
    return pkgutil.find_loader("spacy") is not None

# Check if spaCy is installed
is_spacy_installed = check_spacy_installed()
print(f"spaCy is installed: {is_spacy_installed}")
