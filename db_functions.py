#%%
from datetime import date
from sqlalchemy import TEXT, Date, create_engine
from sqlalchemy import Table, Column, String, MetaData
import pandas as pd
from scrapping import main as scrapping

def engine():
 #Make a connection to the database
    try:
        engine = create_engine("mysql://b4a632817019ce:7058b342@us-cdbr-east-06.cleardb.net/heroku_5073876714a6911?reconnect=true")
    except Exception as e:
        print("Error: Unable to connect to database,","error:",e)
    else:
        print("Connection to database successful")
    return engine

def create_table_db(table_name, engine):
    meta = MetaData()

    table_name = Table(
    f'{table_name}', meta,
    Column('title', String(500), nullable = False),
    Column('link_info', String(500),primary_key = True, nullable = False),
    Column('posting_date', Date, nullable = False),
    Column('closing_date', Date, nullable = False),
    Column('company', String(500), nullable = False),
    Column('location', String(500), nullable = False),
    Column('salary', String(500), nullable = False),
    Column('hours_shifts', String(500), nullable = False),
    Column('type_contract', String(500), nullable = False),
    Column('website_apply', String(500), nullable = False),
    Column('reference', String(500), nullable = False),
    Column('description', TEXT, nullable = False),

    )
    meta.create_all(engine, checkfirst=True)

def read_from_db(table_name,engine):
    sql = f'SELECT * FROM {table_name}'
    df = pd.read_sql(sql, engine)
    return df

def save_data_to_table(data,engine):
    #create temporary table
    create_table_db('jobs_temp',engine)
    print('temporary table created')
    #Save data to temporary table
    data.to_sql('jobs_temp', engine, if_exists='append', index=False)
    print('data saved to temporary table')
    create_table_db('jobs',engine)
    print('table jobs created')
    query = 'SELECT * FROM jobs_temp WHERE link_info NOT IN (SELECT link_info FROM jobs);'
    new_entries = pd.read_sql(query, engine)
    print('new entries found')
    new_entries.to_sql('jobs', engine, if_exists='append', index=False)
    engine.execute('DROP TABLE jobs_temp;')

def get_days(engine):
    query = 'SELECT posting_date FROM jobs ORDER BY posting_date DESC LIMIT 1;'
    try:
        df = pd.read_sql(query, engine)
        last_date = df.iloc[0]['posting_date']
        today = date.today()
        days = (today - last_date).days
    except:
        days = 500
    return days

def main(data,engine):
    #start connection to database
    connection = engine.connect()
    #function to execute
    save_data_to_table(data,engine)
    #Close connection and dispose database
    connection.close()
    engine.dispose()
    print('Closed connection')
#%%
