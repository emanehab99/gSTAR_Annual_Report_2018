import bibtexparser as bibp
import requests
import os


with open('files/ozstar19.bib') as bibfile:
    bibdb = bibp.bparser.BibTexParser(common_strings=True).parse_file(bibfile)

unique_authors = []
total_authors = 0
unique_authors_count = 0

unique_authors_dict = dict()


for entry in bibdb.entries:

    entry_authors = entry['author']
    entry_authors = entry_authors.replace('\n', ' ')
    for author in entry_authors.split('and '):
        total_authors += 1
        if (',' not in author) and (author[-1] == '}'):
            author = author[:-1] + ','

        # oldauthor = author.strip()
        # newauthor = re.sub(r"[\'\"\}\{\^]", "", author.strip())

        author = author.strip().replace('{', '')
        author = author.replace('}', '')
        author = author.replace('\'', '')
        author = author.replace('\"', '')
        author = author.replace('\\', '')
        author = author.replace('^', '')
        author.replace(u"\u2019", "'").strip()

        author = author.split(',')
        if len(author) == 1:
            author.append(' ')
        else:
            author[1] = author[1].strip()

        author = author[:2]

        try:
            exists = False
            print("matching--------------------------------")
            lastname = author[0]
            print("last name: {0}".format(lastname))

            if lastname not in unique_authors_dict.keys():
                unique_authors_dict[lastname] = []
                print("{0} new author".format(unique_authors_dict[lastname]))
            else:
                for name in unique_authors_dict[author[0]]:
                    if author[1][0] == name[1][0]:
                        print("{0} {1} exists".format(author[0], author[1]))
                        exists = True
                        break

            if not exists:
                unique_authors_dict[lastname].append(author)

        except IndexError as e:
            print(e.args)

print("--------------------------------------------------------------------------------------------------------------------")


with open('authors_unique.dat', 'w') as author_file:
    author_file.writelines('Surname,Name\n')
    for lastname in unique_authors_dict:
        for name in unique_authors_dict[lastname]:
            unique_authors_count += 1
            author_file.writelines(','.join(name) + '\n')

print(unique_authors_count)


# count institutions and create file with list of unique institutions

start_tag = '<b>Affiliation:</b></td><td><br></td><td align="left" valign="top">'
end_tag = '</td></tr>\n<tr><td valign="top" align="left"><b>Publication:</b></td><td><br></td><td align="left" valign="top">'

dividers = ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR',
            'AS', 'AT', 'AU', 'AV', 'AZ', 'AX', 'AY', 'AW', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ',
            'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BZ', 'BX', 'BY', 'BW']

##############################################
# Institutions part is not working because the content of ads pages is different and doesn't have the
# affiliations section
# Need to find another way


# unique_institutions = []
#
# for entry in bibdb.entries:
#     try:
#         # print(entry['title'])
#         entry_url = entry['adsurl']
#         if entry_url is not None:
#             page = requests.get(entry_url)
#
#             if start_tag in page.text:
#                 entry_affiliations = page.text.split(start_tag)[1]
#                 entry_affiliations = entry_affiliations.split(end_tag)[0]
#                 for div in dividers:
#                     if (div + '(') in entry_affiliations:
#                         entry_affiliations = entry_affiliations.replace((div + '('), '&&&')
#                 for affil_long in entry_affiliations.split('&&&'):
#                     if len(affil_long.split(', ')) > 2:
#                         affil = affil_long.split(', ')[:3]
#                     else:
#                         affil = [affil_long, '', '']
#                     if affil not in unique_institutions:
#                         unique_institutions.append(affil)
#         else:
#             print(entry['title'])
#
#     except KeyError as e:
#         print(f'error: {e.args}')
#         continue
#
# if os.path.exists('institutions19.dat'):
#     os.remove('institutions19.dat')
#
# for institution in sorted(unique_institutions):
#     with open('institutions19.dat', 'a') as institution_file:
#         institution_file.write(str(institution[0]) + ', ' + str(institution[1]) + '\n')
#     # print str(institution[0]), ', ', str(institution[1])
#
# print('No of unique Institutions', len(unique_institutions))
# institution_file.close()

if __name__ == 'main':
    print('main')
