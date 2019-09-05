import os.path
import pandas as pd
import numpy as np

authors16 = pd.read_csv('files/authors2016', header=0, low_memory=False)
authors17 = pd.read_csv('files/authors2017', header=0, low_memory=False)
authors18 = pd.read_csv('authors_unique.dat', header=0, low_memory=False)
surnames18 = list(authors18['Surname'])

existing = 0
aussies = 0
students = 0

if os.path.exists('authors2018'):
    os.remove('authors2018')

outputfile = open('authors2018', 'w')
outputfile.writelines(["Surname,Name,Nationality,Student\n"])

for surname in surnames18:
    existingauthor17 = authors17.loc[authors17['Surname'] == surname]
    existingauthor16 = authors16.loc[authors16['Surname'] == surname]
    author = authors18.loc[authors18['Surname'] == surname]
    newauthor = ""

    if not existingauthor17.empty:
        nationality = "" if pd.isnull(existingauthor17['Nationality'].values[0]) else existingauthor17['Nationality'].values[0]
        student = "" if pd.isnull(existingauthor17['Student'].values[0]) else existingauthor17['Student'].values[0]

        newauthor = '{0},{1},{2},{3}\n'.format(surname, existingauthor17['Name'].values[0],
                                             nationality, student)

        existing += 1

        if nationality == 'A':
            aussies += 1

        if student:
            students += 1

    elif not existingauthor16.empty:

        nationality = "" if pd.isnull(existingauthor16['Nationality'].values[0]) else \
        existingauthor16['Nationality'].values[0]

        student = "" if pd.isnull(existingauthor16['Student'].values[0]) else existingauthor16['Student'].values[0]


        newauthor = '{0},{1},{2},{3}\n'.format(surname, existingauthor16['Name'].values[0],
                                             nationality, student)

        existing += 1

        if nationality == 'A':
            aussies += 1

        if student:
            print(surname, existingauthor16['Name'].values[0])
            students += 1
    else:
        newauthor = '{0},{1},{2},{3}\n'.format(surname, author['Name'].values[0], "", "")

    outputfile.writelines(newauthor)


outputfile.close()
print(existing)
print("No of Australian co-authors: ", aussies)
print("No of International co-authors: ", existing - aussies)
print("No of Student co-authors: ", students)


