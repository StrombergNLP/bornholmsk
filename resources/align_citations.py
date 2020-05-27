#!/usr/bin/env python3

import nltk
import re
import sys

bo_file = open('citations.da-bo', 'w')
da_file = open('citations.da', 'w')

citationmatcher = r'\<([^\{]+)\{([^\}]+)\}\>'
parenth_stripper = r'\(.+\)'
parenth_only_stripper = r'[\(\)]'
metachars_stripper = r'[#ʁɔː]'
brackets_stripper = r'\[.+?\]'

errors = 0

for line in open(sys.argv[1], 'r'):
	line = line.replace("\n", " ").strip()
	if not line:
		continue
	matches = re.match(citationmatcher, line)
	try:
		bo, da = matches[1], matches[2]
	except:
		errors += 1
		continue

	da = ' '.join(nltk.word_tokenize(da))
	bo = ' '.join(nltk.word_tokenize(bo))
	
	da = re.sub(metachars_stripper, '', da)
	bo = re.sub(metachars_stripper, '', bo)
	
	da = re.sub(brackets_stripper, '', da)
	bo = re.sub(brackets_stripper, '', bo)

	da_flat, bo_flat = re.sub(parenth_only_stripper, '', da), re.sub(parenth_only_stripper, '', bo)
	if da_flat != da or bo_flat != bo:
		da_simple, bo_simple = re.sub(parenth_stripper, '', da), re.sub(parenth_stripper, '', bo)
		if bo_flat.strip() and da_flat.strip():
			bo_file.write(bo_flat + "\n")
			da_file.write(da_flat + "\n")
		if bo_simple.strip() and da_simple.strip():
			bo_file.write(bo_simple + "\n")
			da_file.write(da_simple + "\n")
	else:
		if bo.strip() and da.strip():
			bo_file.write(bo + "\n")
			da_file.write(da + "\n")


print('-- skipped', errors, 'expressions')
