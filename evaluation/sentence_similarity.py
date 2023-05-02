'''
Author: Luke Olson
Uses the sentence transformer library to calculate the cosine similarity between
2 given text files
'''
from sentence_transformers import SentenceTransformer, util
from nltk import sent_tokenize
from os import path

# gather scripts
print('gathering scripts...')
inScript = open(path.abspath(path.join(path.dirname(__file__), '..', 'data', 'American science fiction films.txt')), 'r', encoding ='utf-8')
outScript = open(path.abspath(path.join(path.dirname(__file__), '..', 'data', 'American science fiction films.txt')), 'r', encoding = 'utf-8')
print('done!')

# tokenize (use download('punkt') during first run)
print('tokenizing inputs...')
inSentences = sent_tokenize(inScript.read())
print('done! Tokenizing outputs...')
outSentences = sent_tokenize(outScript.read())
print('done! Creating model...')

# create model
model = SentenceTransformer('all-MiniLM-L6-v2')
print('done!')

#Compute embedding for both lists
print('embedding input sentences...')
embeddings1 = model.encode(inSentences, convert_to_tensor=True)
print('done! embedding output sentences...')
embeddings2 = model.encode(outSentences, convert_to_tensor=True)
print('done!')

#Compute cosine-similarities
print('computing similarities...')
cosine_scores = util.cos_sim(embeddings1, embeddings2)
print('done!')

#Output the pairs with their score
print('averaging scores...')
average = 0
divisor = 0
for i in range(len(inSentences)):
    average += cosine_scores[i][i]
    divisor = i

print("\nOverall score: {}".format(average / (divisor + 1)))