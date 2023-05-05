import os
import pickle
import numpy as np

PATH = '../../../data/Western robot disaster films.txt'

with open(PATH, mode='r', encoding='utf-8') as file:
    data = file.read()
print(f'length of dataset in characters: {len(data):,}')

chars = sorted(list(set(data)))
vocab_size = len(chars)
print('all the unique characters:', ''.join(chars))
print(f'vocab size: {vocab_size:,}')

stoi = { ch: i for i, ch in enumerate(chars) }
itos = { i: ch for i, ch in enumerate(chars) }
def encode(s):
    return [stoi[c] for c in s]
def decode(l):
    return ''.join([itos[i] for i in l])

n = len(data)
train_data = data[:int(n * 0.9)]
val_data = data[int(n * 0.9):]

train_ids = encode(train_data)
val_ids = encode(val_data)
print(f'train has {len(train_ids):,} tokens')
print(f'val has {len(val_ids):,} tokens')

train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)
train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
val_ids.tofile(os.path.join(os.path.dirname(__file__), 'val.bin'))

meta = {
    'vocab_size': vocab_size,
    'itos': itos,
    'stoi': stoi,
}
with open(os.path.join(os.path.dirname(__file__), 'meta.pkl'), 'wb') as f:
    pickle.dump(meta, f)

file.close()