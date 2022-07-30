#%%
from datetime import date
from sqlalchemy import TEXT, Date, create_engine
from sqlalchemy import Table, Column, String, MetaData
import pandas as pd
import os



def engine():
 #Make a connection to the database
    engine = None
    try:
        credentials = os.getenv('DATABASE_URL')
        local_credentials = 'postgresql://p_rw_bd108e58753541558d7cb7e67f434964:bo6lDFn81F--niVd5f1t5loMzJQflhHsf6CJYR0HrnW_dTy7DpIR-u_JxdiCVpl6@pg-tunnel.borealis-data.com:5432/d7587c40f4c6d801c88ed5982d6f219df'
        engine = create_engine(f'{local_credentials}')
        engine.connect()
    except Exception as e:
        print("Error: Unable to connect to database,","error:",e)
    else:
        print("Connection to database successful")
    return engine

def create_table_db(table_name, engine):
    meta = MetaData(engine)

    table_name = Table(
    f'{table_name}', meta,
    Column('title', String(500), nullable = False),
    Column('link_info', String(200), primary_key = True, nullable = False),
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
    #meta.create_all(engine, checkfirst=True)
    table_name.create(checkfirst=True)

def read_from_db(table_name,engine):
    sql = f'SELECT * FROM {table_name}'
    df = pd.read_sql(sql, engine)
    return df

def jobs_count(engine):
    query = 'SELECT COUNT(*) FROM jobs;'
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]

def jobs_available_count(engine):
    query = 'SELECT COUNT(*) FROM jobs WHERE closing_date >= current_date;'
    df = pd.read_sql(query, engine)
    return df.iloc[0][0]

def save_data_to_table(data,engine):
    #Verify if the temporary table exists
    engine.execute('DROP TABLE IF EXISTS jobs_temp;')
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
    print('new entries found:', len(new_entries.index))
    new_entries.to_sql('jobs', engine, if_exists='append', index=False)
    #Delete temporary table
    engine.execute('DROP TABLE IF EXISTS jobs_temp;')

def last_posting_date(engine):
    query = 'SELECT posting_date FROM jobs ORDER BY posting_date DESC LIMIT 1;'
    try:
        df = pd.read_sql(query, engine)
        last_date = df.iloc[0]['posting_date']
    except:
        last_date = date.today()
    return last_date

def get_days(engine):
    query = 'SELECT posting_date FROM jobs ORDER BY posting_date DESC LIMIT 1;'
    try:
        df = pd.read_sql(query, engine)
        last_date = df.iloc[0]['posting_date']
        today = date.today()
        days = (today - last_date).days +1
    except:
        days = 500
    return days

def available_jobs(table_name,engine):
    today = str(date.today())
    sql = f'SELECT * FROM {table_name} WHERE closing_date >= current_date;'
    df = pd.read_sql(sql, engine)
    return df

def main(data,engine):
    #start connection to database
    connection = engine.connect()
    #function to execute
    save_data_to_table(data,engine)
    #Close connection and dispose database
    connection.close()
    engine.dispose()
    print('Closed connection')

def test(engine):
    #start connection to database
    connection = engine.connect()
    #function to execute
    create_table_db('jobs',engine)
    #Close connection and dispose database
    connection.close()
    engine.dispose()
    print('Closed connection')

