#!/usr/bin/env python3
# Generate a text file containing bornholmsk (mixed tokenized and untokenized)
import glob
import os

def ith_line_of_j(f, j, i):
	line_no = 0
	for line in f:
		if line_no % j == i:
			print(line.strip())
		line_no += 1

plain_files = ('bornholmsk.txt', 'bornholmsk_untok.txt')

for filename in plain_files:
	if os.path.isfile(filename):
		for line in open(filename, 'r'):
			line = line.strip()
			if line:
				print(line)

for filename in glob.glob('bo_da_sent*'):
	ith_line_of_j(open(filename, 'r'), 3, 0)


for filename in glob.glob('da_bo_sent*'):
	ith_line_of_j(open(filename, 'r'), 3, 1)
