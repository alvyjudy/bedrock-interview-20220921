import pandas as pd

def cast(x):
    try: 
        return int(x)
    except:
        return 0

def fetch_table():
    return pd.read_html('election.html', match='Results by riding — 2021 Canadian federal election')[0]

def simplify_table(table):
    table = table[[
            ('hideResults by riding — 2021 Canadian federal election[a 1]', 'Winning party', 'Party', 'Party.1'),
            ('hideResults by riding — 2021 Canadian federal election[a 1]', 'Winning party', 'Votes', 'Votes'),
            ('hideResults by riding — 2021 Canadian federal election[a 1]', 'Votes[a 3]', 'Lib', 'Unnamed: 11_level_3'),
            ('hideResults by riding — 2021 Canadian federal election[a 1]', 'Votes[a 3]', 'Con', 'Unnamed: 12_level_3'),
            ('hideResults by riding — 2021 Canadian federal election[a 1]', 'Votes[a 3]', 'NDP', 'Unnamed: 13_level_3'),
            ('hideResults by riding — 2021 Canadian federal election[a 1]', 'Votes[a 3]', 'PPC', 'Unnamed: 16_level_3'),
            ]]
    table.columns = [
        'winning_party_name',
        'winning_party_votes',
        'lib',
        'con',
        'ndp',
        'ppc'
    ]
    name = table['winning_party_name']
    numeric = table.drop('winning_party_name', axis=1).applymap(cast)
    table = pd.concat([name, numeric], axis=1)
    return table

def criteria(party_1, party_2, table):
    return len(table[
        ((table[party_1] + table[party_2]) > table['winning_party_votes']) &
        (table['winning_party_name'] != party_1) &
        (table['winning_party_name'] != party_2)
    ])

def analyze():
    table = fetch_table()
    table = simplify_table(table)
    print("The number of ridings where the combined votes of the CPC (Conservative Party of Canada) and PPC (People's Party of Canada) exceeded that riding's winner's vote total, where the eventual winner was neither of these two parties:", 
    criteria('con', 'ppc', table))
    
    print("The number of ridings where the combined votes of the NDP (New Democratic Party) and PC (Liberal Party of Canada) exceeded that riding's winner's vote total, where the eventual winner was neither of these two parties:", 
    criteria('ndp', 'lib', table))

if __name__ == '__main__':
    analyze()