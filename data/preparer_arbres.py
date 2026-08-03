import numpy as np
import os
import pandas as pd
import sys


def enlever_colonnes(df, colonnes):
    for col in colonnes:
        if col in df.columns:
            df.drop(columns=col, inplace=True)


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

    enlever_colonnes(
        arbres_df, ['NOM_PARC', 'Code_secteur', 'Nom_secteur'])
    parcs_df.dropna().to_csv('arbres_parcs.csv', index=False)


def nettoyage_rues(arbres_df):
    arbres_parcs_df = arbres_df[arbres_df['INV_TYPE'] == 'H'].copy()

    enlever_colonnes(
        arbres_parcs_df,
        [
            'No_civique', 'Rue', 'Rue_cote', 'Rue_de', 'Rue_a',
            'Distance_pave', 'Distance_ligne_rue',
            'District', 'LOCALISATION', 'Localisation_code',
            'Stationnement_jour', 'Stationnement_heure',
            'INV_TYPE',
        ]
    )

    return arbres_parcs_df


def nettoyage_coordonnees(arbres_parcs_df):
    for c in ['Longitude', 'Latitude']:
        mediane = arbres_parcs_df[c].median()
        dev_std = arbres_parcs_df[c].std()
        arbres_parcs_df = arbres_parcs_df[
            np.abs(arbres_parcs_df[c] - mediane) < 3 * dev_std
        ]

    enlever_colonnes(arbres_parcs_df, ['Coord_X', 'Coord_Y'])

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
    arbres_plantation_df = arbres_parcs_df.dropna().drop(
        columns='Date_Releve').copy()

    arbres_plantation_df.to_csv('arbres_inv.csv', index=False)


def preparer_arbres():
    arbres_df = pd.read_csv(
        'arbres-publics.csv',
        dtype={col_name: 'str' for col_name in [
            'CODE_PARC',
            'Distance_ligne_rue',
            'LOCALISATION',
            'Localisation_code',
            'NOM_PARC',
            'Nom_secteur',
            'No_civique',
            'Rue',
            'Rue_a',
            'Rue_cote',
            'Rue_de',
            'Stationnement_jour',
            'Stationnement_heure',
        ]}
    )

    arbres_df.drop(columns='ARROND_NOM', inplace=True)
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
    arrond_df.to_csv('arbres_arrondissements.csv')


def main():
    os.chdir(sys.path[0])

    preparer_arrond()
    preparer_arbres()


if __name__ == '__main__':
    main()
