import bibtexparser as bibp

import requests

import sys

# surname = sys.argv[1]

# with open('files/ozstar18.bib') as bibtex_file:
# 	bibtex_str = bibtex_file.read()
# bib_database = bibp.loads(bibtex_str)

with open('files/ozstar18.bib') as bibfile:
	bib_database = bibp.bparser.BibTexParser(common_strings=True).parse_file(bibfile)



start_tag = '<b>Affiliation:</b></td><td><br></td><td align="left" valign="top">'
end_tag = '</td></tr>\n<tr><td valign="top" align="left"><b>Publication:</b></td><td><br></td><td align="left" valign="top">'

dividers = ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ']

# for entry in bib_database.entries:
# 	entry_url = entry['adsurl']
# 	entry_authors = entry['author']
# 	entry_authors = entry_authors.replace('\n', ' ')
# 	entry_authors_array = entry_authors.split('and ')
# 	for author in entry_authors_array:
# 		if surname in author:
# 			i = entry_authors_array.index(author)
# 			div_1 = dividers[i] + '('
# 			div_2 = dividers[i+1] + '('
# 			page = requests.get(entry_url)
# 			if start_tag in page.content:
# 				affiliations_tag = page.content.split(div_1)[1]
# 				affiliations_tag = affiliations_tag.split(end_tag)[0]
# 				affiliations = affiliations_tag.split(div_2)[0]
#
# 				print(surname, affiliations)
# 				if affiliations.count('Australia') > 0:
# 					print('Australia')
# 				else:
# 					print('International')

international_collaboration = 0
multiple_aus_institutes = 0

for entry in bib_database.entries:
	try:

		entry_url = entry['adsurl']
		page = requests.get(entry_url)

		if start_tag in page.text:
			entry_affiliations = page.text.split(start_tag)[1]
			entry_affiliations = entry_affiliations.split(end_tag)[0]

			n = entry_affiliations.count('Australia')
			if n>1:
				multiple_aus_institutes = multiple_aus_institutes + 1

			for div in dividers:
				if (div+'(') in entry_affiliations:
					entry_affiliations = entry_affiliations.replace((div+'('), '&&&')

			tot_affil = len(entry_affiliations.split('&&&'))

			if (n>0) and (n<tot_affil):
				international_collaboration = international_collaboration + 1
	except KeyError as e:
		print("KeyError: " + e.args)
		continue
		
print('International collaborations:', international_collaboration)
print('Multiple Australian Institutes:', multiple_aus_institutes)
