#%%

from db_functions import main as save_to_db
from db_functions import engine as engine_db
from db_functions import read_from_db as read_from_db
from db_functions import get_days as get_days
from scrapping import get_last_page as get_last_page
from scrapping import iterate_jobs_in_page as iterate_jobs_in_page

def main():
    # Get connection to database
    engine = engine_db()
    #Get days to scrap and url
    days = get_days(engine)
    print(f'Days to scrap: {days}')
    url = f'https://findajob.dwp.gov.uk/search?pp=50&f={days}'
    #Scrapping the website
    print('Start scrapping')
    last_page = int(get_last_page(url))
    print(f'total pages: {last_page}')
    # Iterate through all the pages
    for page in range (last_page, 0, -1):
        print('----------------------')
        print(f'Start scrapping page {page} ')
        page_url = f'{url}&page={page}'
        #scrap each page and save the data in a dataframe
        jobs_details_for_page = iterate_jobs_in_page(page_url)
        jobs_details_for_page.fillna('None', inplace=True)
        print(f'page {page} is scraped')
        #Save data from each page to db
        save_to_db(jobs_details_for_page,engine)
        print(f'page {page} is saved to db')
    print('Scrapping is done')

#%%
main()

# %%
#days to scrap 111