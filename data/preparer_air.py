import numpy as np
import os
import pandas as pd
import sys


def charger_donnees(debug_level=0):
    air_df_list = []

    for periode in ['2023', '2024']:
        fichier_csv = f'mesure-impact-projets-verdissement-{periode}.csv'
        air_df = pd.read_csv(fichier_csv)

        air_df['date_heure'] = pd.to_datetime(
            air_df['date_heure'],
            format='%m/%d/%y %H:%M:%S' if periode == '2024' else None
        )

        air_df_list.append(air_df)

    for periode in ['janv-juin-2025', 'juil-dec-2025']:
        fichier_csv = f'mesure-impact-projets-verdissement-{periode}.csv'
        air_df = pd.read_csv(fichier_csv, sep=';', decimal=',')

        air_df['date_heure'] = pd.to_datetime(
            air_df['date_heure'],
            format='%m/%d/%y %H:%M:%S %z',
            utc=True
        ).dt.tz_convert(None)

        for nom_colonne in ['longitude', 'latitude']:
            air_df[nom_colonne] = air_df[nom_colonne].astype('float')

        air_df_list.append(air_df)

    if debug_level >= 1:
        for air_df in air_df_list:
            print(air_df.dtypes)

    return pd.concat(air_df_list).reset_index(drop=True)


def enlever_colonnes(df, colonnes):
    for nom_colonne in colonnes:
        df.drop(columns=nom_colonne, inplace=True)


def preparer_stations(air_df):
    id_stations = air_df['id_station'].str.replace('-1$', '', regex=True)
    id_stations = id_stations.str.split().str[1]  # '12345678:87654321'
    id_stations = id_stations.str.split(':').str[0]  # '12345678'
    id_stations = id_stations.astype('int')  # 12345678
    air_df['id_station'] = id_stations

    air_df['nom_station'] = air_df['nom_station'].str.replace('é', 'e')

    masque_e67 = (
        (air_df['id_station'] == 21317941) &
        (air_df['nom_station'] == 'Espace_67')
    )
    air_df.loc[masque_e67, 'nom_station'] = 'Carref_Langelier'

    masque_jde = (
        (air_df['nom_station'] == 'Jean-Drapeau_Etang') &
        (air_df['longitude'] == -73.556306)
    )
    air_df.loc[masque_jde, 'longitude'] = -73.532472
    air_df.loc[masque_jde, 'latitude'] = 45.518028

    stations_df = air_df[
        ['id_station', 'nom_station', 'longitude', 'latitude']
    ].drop_duplicates().sort_values('id_station')

    stations_df.to_csv('air_stations.csv', index=False)
    enlever_colonnes(air_df, stations_df.columns[1:])


def nettoyer_mesures(air_df):
    temp_rh_dp = air_df.set_index(['id_station', 'date_heure']).dropna().copy()

    mediane = temp_rh_dp['temperature'].median()
    dev_std = temp_rh_dp['temperature'].std()

    temp_rh_dp = temp_rh_dp[
        np.abs(temp_rh_dp['temperature'] - mediane) < 3 * dev_std
    ]

    return temp_rh_dp


def preparer_points_rosee(temp_rh_dp):
    points_rosee = temp_rh_dp.copy()

    points_rosee['temperature'] = \
        points_rosee['temperature'].round().astype('int')
    points_rosee['RH'] = \
        ((points_rosee['RH'] / 5).round() * 5).astype('int')

    points_rosee.groupby(
        ['temperature', 'RH']
    ).mean().round(1).to_csv('air_points_rosee.csv')

    return temp_rh_dp[['temperature', 'RH']].reset_index()


def preparer_air():
    air_df = charger_donnees()

    preparer_stations(air_df)

    temp_rh_dp = nettoyer_mesures(air_df)
    temp_rh = preparer_points_rosee(temp_rh_dp)


def main():
    os.chdir(sys.path[0])

    preparer_air()


if __name__ == '__main__':
    main()
