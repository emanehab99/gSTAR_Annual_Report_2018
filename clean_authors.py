import pandas as pd

authors_df = None

def read_authors(authors_file):
    authors_df = pd.read_csv(authors_file)

def existing_author(lastname, firstname):

    return False


