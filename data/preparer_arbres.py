import numpy as np
import os
import pandas as pd
import sys


def enlever_colonnes(df, colonnes):
    for nom_colonne in colonnes:
        df.drop(columns=nom_colonne, inplace=True)


def preparer_essences(arbres_df):
    essences_df = arbres_df[
        ['Sigle', 'Essence_latin', 'Essence_ang', 'Essence_fr']
    ].drop_duplicates().sort_values('Sigle')

    enlever_colonnes(arbres_df, essences_df.columns[1:])
    essences_df.to_csv('arbres_essences.csv', index=False)


def preparer_parcs(arbres_df):
    parcs_df = arbres_df[
        ['CODE_PARC', 'NOM_PARC']
    ].drop_duplicates().sort_values('CODE_PARC')

    enlever_colonnes(arbres_df, ['NOM_PARC'])
    parcs_df.dropna().to_csv('arbres_parcs.csv', index=False)


def nettoyage_rues(arbres_df):
    arbres_parcs_df = arbres_df[arbres_df['INV_TYPE'] == 'H'].copy()
    enlever_colonnes(arbres_parcs_df, ['INV_TYPE'])

    return arbres_parcs_df


def nettoyage_coordonnees(arbres_parcs_df):
    for nom_colonne in ['Longitude', 'Latitude']:
        mediane = arbres_parcs_df[nom_colonne].median()
        dev_std = arbres_parcs_df[nom_colonne].std()

        arbres_parcs_df = arbres_parcs_df[
            np.abs(arbres_parcs_df[nom_colonne] - mediane) < 3 * dev_std
        ]

    return arbres_parcs_df


def preparer_emplacements(arbres_parcs_df):
    col_type_emp, col_type_emp_id = 'Emplacement', 'type_emp_id'

    arbres_parcs_df[col_type_emp], noms_type_emp = \
        arbres_parcs_df[col_type_emp].factorize(sort=True)
    arbres_parcs_df.rename(
        columns={col_type_emp: col_type_emp_id}, inplace=True)

    type_emp_df = pd.DataFrame(
        noms_type_emp.str.capitalize(),
        columns=[col_type_emp]
    )
    type_emp_df.index.name = col_type_emp_id
    type_emp_df.to_csv('arbres_emplacements.csv')


def preparer_plantations(arbres_parcs_df):
    arbres_plantation_df = arbres_parcs_df.dropna().copy()
    arbres_plantation_df.to_csv('arbres_inv.csv', index=False)


def preparer_arbres():
    arbres_df = pd.read_csv(
        'arbres-publics.csv',
        usecols=[
            'INV_TYPE', 'EMP_NO', 'ARROND', 'Emplacement',
            'Sigle', 'Essence_latin', 'Essence_ang', 'Essence_fr',
            'DHP', 'Date_Plantation', 'CODE_PARC', 'NOM_PARC',
            'Arbre_remarquable', 'Longitude', 'Latitude'
        ],
        dtype={
            'CODE_PARC': 'str',
            'NOM_PARC': 'str',
        }
    )

    arbres_df.rename(columns={'ARROND': 'arrond_id'}, inplace=True)

    preparer_essences(arbres_df)
    preparer_parcs(arbres_df)

    arbres_parcs_df = nettoyage_rues(arbres_df)
    arbres_parcs_df = nettoyage_coordonnees(arbres_parcs_df)

    preparer_emplacements(arbres_parcs_df)
    preparer_plantations(arbres_parcs_df)


def preparer_arrond():
    index_col='Numéro '

    arrond_df = pd.read_csv(
        'etatinventaire_arbrespublics_pararrondissement.csv',
        index_col=index_col,
        usecols=[index_col, 'Arrondissement'],
    )

    arrond_df.index.name = 'arrond_id'
    arrond_df.to_csv('mtl_arrondissements.csv')


def main():
    os.chdir(sys.path[0])

    preparer_arrond()
    preparer_arbres()


if __name__ == '__main__':
    main()
