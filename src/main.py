import mysql.connector
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, playergamelogs, leaguegamelog
from data import fetch_data as fd
from config import sql_setup as sql
from data import load_data as load
from data import convert_data as cd
from scripts import train_model_two as tm
import numpy as np
import pandas as pd

import os

def connect_to_db():
    host = os.getenv('DB_HOST', '127.0.0.1')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'your_default_password')
    database = os.getenv('DB_NAME', 'nba_data')

    try:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None



def main():
    db_connection = connect_to_db()
    cursor = db_connection.cursor()

    sql.create_tables(cursor)
    db_connection.commit()

    # fetch data
    seasons = ['1976-77', '1977-78','1978-79', '1979-80',
               '1980-81', '1981-82','1982-83', '1983-84',
               '1984-85', '1985-86', '1986-87','1987-88',
               '1988-89','1989-90','1991-92', '1992-93',
               '1993-94', '1994-95', '1995-96',
                '1996-97', '1997-98', '1998-99', '1999-00',
                '2000-01', '2001-02', '2002-03', '2003-04',
                '2004-05', '2005-06', '2006-07', '2007-08',
                '2008-09', '2009-10', '2010-11', '2011-12',
                '2012-13', '2013-14', '2014-15', '2015-16',
                '2016-17', '2017-18','2018-19','2019-20',
                '2020-21', '2021-22', '2022-23']
    for year in seasons:
        print(f"Processing data for the {year} season...")
        fd.fetchTeamsforSeason(cursor, db_connection)  
        fd.fetchGamesForSeason(year, cursor, db_connection)  
        fd.fetchPlayersforSeason(year, cursor, db_connection) 
        fd.fetchPlayerSeasonAverages(year, cursor, db_connection)
        db_connection.commit()
        print("Successfully processed data for the {year} season.")

    #load data
    nba_dataframe = load.getData(cursor)
    pd.set_option('display.max_columns', None)
    print("Data loaded successfully.")

    nan_counts = nba_dataframe.isnull().sum()
    

    train_data, test_data = cd.prepare_tensors(nba_dataframe)
    print("Data converted to tensors.")

    tm.train_model(train_data, test_data)


    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
