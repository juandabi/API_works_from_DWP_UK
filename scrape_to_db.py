#%%

from db_functions import main as save_to_db
from db_functions import engine as engine_db
from db_functions import read_from_db as read_from_db
from db_functions import get_days as get_days
from scrapping import main as scrapping



def main():
    # Get connection to database
    engine = engine_db()
    #Scrapping the website
    days = get_days(engine)
    url = f'https://findajob.dwp.gov.uk/search?pp=50&f={days}'
    scrapping_data = scrapping(url)
    # execute function to save data to database
    #engine = engine_db()
    save_to_db(scrapping_data,engine)
    # read data from database
    print("data saved to database")

main()
