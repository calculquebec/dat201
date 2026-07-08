import os
import pandas as pd
import sys


def count_by(df, col):
    filename = f'velos_par_{col}.csv'
    print(f'Creating {filename}...')

    df.pivot_table(
        values='nb_passages', aggfunc='sum',
        index=[col, 'id_compteur']
    ).to_csv(filename)


def main():
    os.chdir(sys.path[0])

    velos_df = pd.read_csv(
        'comptage_velo_2025.csv',
        usecols=['date', 'heure', 'id_compteur', 'nb_passages'],
        dtype={'id_compteur': 'str'})

    velos_df['nb_passages'] = velos_df['nb_passages'].fillna(
        0).astype('int')

    count_by(velos_df, 'date')
    count_by(velos_df, 'heure')


if __name__ == '__main__':
    main()
