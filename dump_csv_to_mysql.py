import pandas as pd
from decouple import config

username = config("MYSQL_USER")
password = config("MYSQL_PASSWORD")

# insert data from csv file into dataframe.
# working directory for csv file: type "pwd" in Azure Data Studio or Linux
# working directory in Windows c:\users\username
df = pd.read_csv("NFL/Data/processed_game_history.csv")
df = df.drop("Unnamed: 0", axis=1)
df = df.rename(columns={'Week': 'GameWeek', 'Day': 'GameDayOfWeek', 'Date': 'GameDate',
                        'Winner/tie': 'WinnerTie', 'Loser/tie': 'LoserTie', 'ModifiedWeek': 'ModifiedGameWeek',
                        "AtHome": "HomeTeam"})

import sqlalchemy as db
# specify database configurations

db_user = config("MYSQL_USER")
db_pwd = config("MYSQL_PASSWORD")
db_host = config("db_host")
db_port = config("db_port")
db_name = config("db_name")
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

# connect to database
engine = db.create_engine(connection_str)
#connection = engine.connect()# pull metadata of a table
#metadata = db.MetaData(bind=engine)
#metadata.reflect(only=['processedresults'])

#test_table = metadata.tables['processedresults']

#print(test_table)

# Insert whole DataFrame into MySQL
df.to_sql('processedresults', con = engine, if_exists = 'append', chunksize = 1000, index = False)
