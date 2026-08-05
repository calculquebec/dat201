import numpy as np
import os
import pandas as pd
import sys


def main():
    os.chdir(sys.path[0])

    permis_df = pd.read_csv('statistiques-permis-de-construction.csv')
    arrond_id = pd.read_csv(
        'mtl_arrondissements.csv',
        index_col='Arrondissement'
    )['arrond_id']

    permis_df['arrondissement'] = permis_df['arrondissement'].apply(
        lambda nom_arrond: arrond_id[nom_arrond])
    permis_df.rename(columns={'arrondissement': 'arrond_id'}, inplace=True)

    permis_1990_CO_DE = permis_df[
        (permis_df['annee'] == 1990) &
        permis_df['code_type_base_demande'].isin(['CO', 'DE'])
    ]

    # Seul l'enregistrement 29 a une valeur non définie
    sommes = permis_1990_CO_DE.sum()
    permis_df.loc[29, 'cout_permis_emis'] = np.round(
        sommes['cout_permis_emis'] / sommes['nombre_permis_emis'],
        decimals=2
    )

    permis_df.to_csv('construction_permis.csv', index=False)


if __name__ == '__main__':
    main()
