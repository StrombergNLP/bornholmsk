#!/usr/bin/env python3

import nltk
import sys

a = None
b = None
infilename = sys.argv[1]
next_line_is_a = True

outfile_a = open(infilename + '.a', 'w')
outfile_b = open(infilename + '.b', 'w')


for line in open(infilename, 'r'):
	line = ' '.join(nltk.word_tokenize(line.strip()))
	if next_line_is_a:
			outfile_a.write(line + "\n")
			next_line_is_a = False

	else:
		if line:
			outfile_b.write(line + "\n")
		else:
			next_line_is_a = True

outfile_a.close()
outfile_b.close()