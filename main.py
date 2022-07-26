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
    #Scrapping the website
    days = get_days(engine)
    url = f'https://findajob.dwp.gov.uk/search?pp=50&f={days}'
    scrapping_data = scrapping(url)

    # execute function to save data to database
    save_to_db(scrapping_data,engine)
    # read data from database
    df = read_from_db('jobs',engine)
    data = df.to_dict(orient='records')
    return data
