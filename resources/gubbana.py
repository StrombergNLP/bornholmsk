#!/usr/bin/env python3

import bs4
soup = bs4.BeautifulSoup(open('view-source_gubbana.dk_borrinjholmsk_.html','r'), features='html.parser')

c1 = soup.find_all('td', {'class':'column-1'})
c2 = soup.find_all('td', {'class':'column-2'})
c3 = soup.find_all('td', {'class':'column-3'})
c4 = soup.find_all('td', {'class':'column-4'})
c5 = soup.find_all('td', {'class':'column-5'})

tokpair_file = open('bo_da_word_gubbana.tsv', 'w')
sentpair_file = open('bo_da_sent_gubbana.txt', 'w')
for i in range(len(c1)):
	tokpair_file.write(c1[i].text.lower() + "\t" + c2[i].text.lower() + "\n")
	sentpair_file.write("\n".join([c3[i].text, c4[i].text, '', ''])  )

tokpair_file.close()
sentpair_file.close()