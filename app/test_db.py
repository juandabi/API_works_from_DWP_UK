import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def engine(databaseconfig):
    # Make a connection to the database
    engine = None
    try:
        engine = create_engine(databaseconfig)
        engine.connect()
    except Exception as e:
        print("Error: Unable to connect to database,", "error:", e)
    else:
        print("Connection to database successful")
    return engine


credentials = os.getenv("DATABASE_URL_LOCALHOST")
print(credentials)
engine(credentials)
