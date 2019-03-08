#!/usr/bin/env python3

import argparse
from fasttext import FastVector
import sys

p = argparse.ArgumentParser()
p.add_argument('-s', '--source', help='the embeddings to be adjusted', required=True)
p.add_argument('-t', '--target', help='the destination embedding space', required=True)
p.add_argument('-d', '--biling_dict', help='path to bilingual dict TSV file')
p.add_argument('-v', '--verbose', help='give extra output', action="store_true")
args = p.parse_args()

print('loading vecs')
source_vecs = FastVector(vector_file=args.source)
target_vecs = FastVector(vector_file=args.target)
source_words = set(source_vecs.word2id.keys())
target_words = set(target_vecs.word2id.keys())

print('evaluating against', args.biling_dict)
eval_pairs_count = 0
vecsims = []
for line in open(args.biling_dict, 'r'):
	line = line.strip()
	if not line:
		continue
	parts = line.split('\t')
	if len(parts) != 2:
            print('entry with |args|≠2:', line)
            continue
	source_word, target_word = parts
	if ' ' in source_word + target_word:
		continue
	if source_word not in source_words or target_word not in target_words:
		continue

	source_vec = source_vecs[source_word]
	target_vec = target_vecs[target_word]
	vecsim = FastVector.cosine_similarity(source_vec, target_vec)

	if args.verbose:
		print(' vecsim:', source_word, target_word, vecsim)

	vecsims.append(vecsim)

print('mean vecsim:', sum(vecsims) / len(vecsims), 'entries used:', len(vecsims))