#!/usr/bin/env python3
import nltk
import numpy as np
import sys

def subchunks(l, n):
	# return chunks of length n from list l
	return [l[y:y+n] for y in range(len(l)-(n-1)) ]

def list_overlap(a, b):
	a = list(a)
	# how many of b are in a?
	start_size = len(a)
	for item in b:
		try:
			a.remove(item)
		except:
			pass
	return start_size - len(a)

def overlap(a,b):
	#compute character-level bleu, for n from [1,3]
	bigrams_a = subchunks(a, 2)
	bigrams_b = subchunks(b, 2)

	trigrams_a = subchunks(a, 3)
	trigrams_b = subchunks(b, 3)

	uni_component = list_overlap(a,b)
	bi_component = list_overlap(bigrams_a, bigrams_b)
	tri_component = list_overlap(trigrams_a, trigrams_b)

	bleu = np.power(uni_component/len(b) + bi_component/len(bigrams_b) + tri_component/len(trigrams_b), 1/3)
	return bleu

def da_norm(sent):
	sent = sent.replace('aa', 'å')
	sent = sent.replace('Aa', 'Å')
	sent = sent.replace('ee', 'é')
	sent = sent.replace('Ee', 'É')
	return sent

da_text = ''
bo_text = ''

da_sents = ''
bo_sents = ''

infilename = sys.argv[1]
infile = open(infilename, 'r')

lang_is_bo = True

for line in infile:
	if line.strip():
		line = line.replace('\n', ' ')
		if lang_is_bo == True:
			bo_text += line
		else:
			da_text += line
	else:
		lang_is_bo = not lang_is_bo

da_sents = nltk.sent_tokenize(da_text)
bo_sents = nltk.sent_tokenize(bo_text)

# 1 = plain, 2 = with Danish oe ae aa ee normalised, 3 = as 2 but all lowercase
bo_outfile = open(infilename + ".plain.da-bo", 'w')
da_outfile_1 = open(infilename + ".plain.da", 'w')
da_outfile_2 = open(infilename + ".norm.da", 'w')
da_outfile_3 = open(infilename + ".norm.lc.da", 'w')

for i in range(len(bo_sents)):
	o = overlap(bo_sents[i], da_sents[i])
	if o < 1:
		print('-' * 40)
	print(bo_sents[i])
	print(da_sents[i])
	print('#', i, ':', o)
	print()
	bo_outfile.write(' '.join(nltk.word_tokenize(bo_sents[i])) + "\n")
	da_outfile_1.write(' '.join(nltk.word_tokenize(da_sents[i])) + "\n")
	da_outfile_2.write(da_norm(' '.join(nltk.word_tokenize(da_sents[i]))) + "\n")
	da_outfile_3.write(da_norm(' '.join(nltk.word_tokenize(da_sents[i]))).lower() + "\n")

for f in (bo_outfile, da_outfile_1, da_outfile_2, da_outfile_3):
	f.close()
