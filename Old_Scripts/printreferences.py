import bibtexparser
import os.path
import pandas as pd

authors = pd.read_csv('authors2017', header=0, low_memory=False)
surnames = list(authors['Surname'])
nationalities = list(authors['Nationality'])
# print nationalities


with open('gstar17.bib') as bibtex_file:
	bibtex_str = bibtex_file.read()
bib_database = bibtexparser.loads(bibtex_str)

	
if os.path.exists('printreferences.out'):
	os.remove('printreferences.out')

outputfile = open('printreferences.out', 'w')

print "no of references:", len(bib_database.entries)

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


	outputfile.write( '\\emph{' + entry['title'] + '}, ',  )
	outputfile.write( entry['journal'] + ', ',	       )

	if 'volume' in entry.keys():
		outputfile.write( 'Volume ' + entry['volume'] + ', ',  )

	if 'pages' in entry.keys():
		outputfile.write( 'Pages ' + entry['pages'] + ', ',    )


	outputfile.write( entry['year'],		       )
	outputfile.write( '\n',				       )


outputfile.close()


