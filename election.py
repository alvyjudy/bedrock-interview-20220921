import pandas as pd # library for data analysis

def fetch_table():
    with open('election.html') as html:
        pd.read_html(html)


