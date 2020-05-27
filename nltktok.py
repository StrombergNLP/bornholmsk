#!/usr/bin/env python3
import nltk
import sys

for line in open(sys.argv[1], 'r'):
  print(' '.join(nltk.word_tokenize(line.strip())))

