#%%
from fastapi import FastAPI
from db_functions import main as save_to_db
from db_functions import engine as engine_db
from db_functions import read_from_db as read_from_db
from db_functions import get_days as get_days
from scrapping import main as scrapping


app = FastAPI()


@app.get("/")
async def root():
    # Get connection to database
    engine = engine_db()
    # read data from database
    df = read_from_db('jobs',engine)
    data = df.to_dict(orient='records')
    return data
