import spacy

# pip install -U pip setuptools wheel
# pip install -U 'spacy[cuda11x]'
# python -m spacy download en_core_web_sm


nlp = spacy.load("en_core_web_sm")

text = "running dogs are happily barking"

doc = nlp(text)

for token in doc:
    print(token.lemma_)