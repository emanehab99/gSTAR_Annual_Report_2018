import bibtexparser
import os.path
import requests


with open('gstar17.bib') as bibtex_file:
	bibtex_str = bibtex_file.read()
    
# count authors and create file with list of unique authors        

bib_database = bibtexparser.loads(bibtex_str)

unique_authors = []

tot_authors=0
for entry in bib_database.entries:
	entry_authors = entry['author']
	entry_authors = entry_authors.replace('\n', ' ')
	for author in entry_authors.split('and '):
		tot_authors = tot_authors+1
		#if author[0] == '{':
		#	author = author[1:]
		#if '},' in author:
		#	author = author.replace('},', ',')	
		if (',' not in author) and (author[-1] == '}'):
			author = author[:-1] + ','
		author = author.replace('{', '') 		
		author = author.replace('}', '') 		
		author = author.replace('\'', '')		
		author = author.replace('\"', '')		
		author = author.replace('\\', '') 
		author = author.replace('^', '') 		
		if author not in unique_authors:
			unique_authors.append(author)

print 'Total number of bibtex entries:', len(bib_database.entries)
print 'Total number of co-authors:', tot_authors
print 'Number of unique co-authors:', len(unique_authors)

if os.path.exists('authors.dat'):
	os.remove('authors.dat')


for author in unique_authors:
	with open('authors.dat', 'a') as author_file:
		# print author
		author_file.write(author.replace(u"\u2019", "'") + '\n')
	
author_file.close()

# count institutions and create file with list of unique institutions   

start_tag = '<b>Affiliation:</b></td><td><br></td><td align="left" valign="top">'
end_tag = '</td></tr>\n<tr><td valign="top" align="left"><b>Publication:</b></td><td><br></td><td align="left" valign="top">'

dividers = ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AZ', 'AX', 'AY', 'AW', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BZ', 'BX', 'BY', 'BW']

unique_institutions = []

for entry in bib_database.entries:
	print entry['title']
	entry_url = entry['adsurl']     
	page = requests.get(entry_url)

	if start_tag in page.content:
		entry_affiliations = page.content.split(start_tag)[1]
		entry_affiliations = entry_affiliations.split(end_tag)[0]
		for div in dividers:
			if (div+'(') in entry_affiliations:
				entry_affiliations = entry_affiliations.replace((div+'('), '&&&')
		for affil_long in entry_affiliations.split('&&&'):
			if len(affil_long.split(', '))>2:
				affil = affil_long.split(', ')[:3]
			else:
				affil = [affil_long, '','']	
			if affil not in unique_institutions:
				unique_institutions.append(affil)

if os.path.exists('institutions.dat'):
	os.remove('institutions.dat')

for institution in sorted(unique_institutions):
	with open('institutions.dat', 'a') as institution_file:
		institution_file.write(str(institution[0]) + ', ' + str(institution[1]) + '\n')
		# print str(institution[0]), ', ', str(institution[1])

print 'No of unique Institutions', len(unique_institutions)
	
institution_file.close()


