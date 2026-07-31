#import numpy as np
import os
import pandas as pd
import sys


def preparer_arrond():
    index_col='Numéro '

    arrond_df = pd.read_csv(
        'etatinventaire_arbrespublics_pararrondissement.csv',
        index_col=index_col,
        usecols=[index_col, 'Arrondissement'],
    )

    arrond_df.index.name = 'arrond_id'
    arrond_df.to_csv('arbres_arrondissements.csv')


def main():
    os.chdir(sys.path[0])

    preparer_arrond()


if __name__ == '__main__':
    main()
