import bibtexparser as bibp
import os.path
import pandas as pd

authors = pd.read_csv('authors_2018_1', header=0, low_memory=False)
surnames = list(authors['Surname'])
nationalities = list(authors['Nationality'])
# print nationalities


with open('files/ozstar18.bib') as bibfile:
	bib_database = bibp.bparser.BibTexParser(common_strings=True).parse_file(bibfile)

	
if os.path.exists('printreferences_test.out'):
	os.remove('printreferences_test.out')

outputfile = open('printreferences_test.out', 'w')

print("no of references:", len(bib_database.entries))

for entry in bib_database.entries:

	entry_authors = entry['author']
	entry_authors = entry_authors.replace('\n', ' ')
	outputfile.write('\\item ',)
	for author in entry_authors.split('and '):
		author = author.replace('{', '')
		author = author.replace('}', '')
		author = author.replace('\'', '')
		author = author.replace('\"', '')
		author = author.replace('\\', '')
		author = author.replace('^', '')
		nationality = 'meh'
		if author.split(',')[0] in surnames:
			index = surnames.index(author.split(',')[0])
			nationality = nationalities[index]
		if nationality == 'A':
			# print '{\\bf ' + author[:-1] + '}; ',
			outputfile.write('{\\bf ' + author[:-1] + '}; ',)
		else:
			# print author[:-1] + '; ',
			outputfile.write(author[:-1] + '; ',)

	# print '\\emph{' + entry['title'] + '},',
	# print entry['journal'] + ',',
	# print 'Volume ' + entry['volume'] + ',',
	# print 'Pages ' + entry['pages'] + ',',
	# print entry['year'],
	# print '\n',


	outputfile.write('\\emph{' + entry['title'] + '}')
	# outputfile.write(entry['journal'] + ', ')

	if 'journal' in entry.keys():
		outputfile.write(', Journal ' + entry['journal'])

	if 'volume' in entry.keys():
		outputfile.write(', Volume ' + entry['volume'])

	if 'pages' in entry.keys():
		outputfile.write(', Pages ' + entry['pages'])

	if 'year' in entry.keys():
		outputfile.write(', Year ' + entry['year'])


	outputfile.write('\n')


outputfile.close()


