'''
Author: Luke Olson
Uses the sentence transformer library to calculate the cosine similarity between
2 given text files
'''
from sentence_transformers import SentenceTransformer, util
from nltk import sent_tokenize, download
from pandas import DataFrame
from plotly.express import line
import glob

samplingDir = '../nanoGPT/out-sciences_fiction'
scriptPath = '../data/American science fiction films.txt'

def findSimilarity(inPath, outPath):
    # gather scripts
    inScript = open(inPath, mode = 'r', encoding ='utf-8')
    outScript = open(outPath, mode = 'r', encoding ='utf-8')

    # tokenize (use download('punkt') during first run)

    inSentences = sent_tokenize(inScript.read())
    outSentences = sent_tokenize(outScript.read())

    # create model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    #Compute embedding for both lists
    embeddings1 = model.encode(inSentences, convert_to_tensor=True)
    embeddings2 = model.encode(outSentences, convert_to_tensor=True)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    #Average scores
    average = 0
    divisor = 0
    for i in range(len(inSentences)):
        average += cosine_scores[i][i]
        divisor = i + 1

    return average / divisor

def plot(data):
    df = DataFrame(data)
    fig = line(df, x='iter', y='similarity', title='Similarity to Scripts Over Iterations')
    fig.show()

if __name__ == '__main__':
    data = { 'iter': [], 'similarity': [] }
    extract_number = lambda s: int(''.join(filter(str.isdigit, s)))
    for filePath in sorted(glob.glob(f'{samplingDir}/*.txt'), key=extract_number):
        similarities = findSimilarity(scriptPath, filePath)
        data['iter'].append(extract_number(filePath))
        data['similarities'].append(similarities)
    plot(data)