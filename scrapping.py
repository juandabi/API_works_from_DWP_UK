#%%
import pandas as pd
from datetime import datetime

import requests
from bs4 import BeautifulSoup

def create_dictionary(title, link_info, posting_date,closing_date, company, location, salary, hours_shifts, type_contract, website_apply, reference, description):
    """
    Create a dictionary of the jobs details
    input: title,  posting_date,closing_date, company, location, salary, hours_shifts,type_contract, description, link_info,reference,website_apply
    Return: dictionary of jobs details
    """
    # Create a dictionary of the jobs details
    job_details = {
        'title': title,
        'posting_date': posting_date,
        'closing_date': closing_date,
        'company': company,
        'location': location,
        'salary': salary,
        'type_contract': type_contract,
        'link_info': link_info,
        'website_apply': website_apply,
        'hours_shifts': hours_shifts,
        'description': description,
        'reference': reference,
    }
    return job_details

def get_last_page(url):
    """
    Get the last page of the website
    input: url
    return: last page
    """
    # get request from the website
    html_text = requests.get(url).text
    # Using beautiful soup to parse the html
    soup = BeautifulSoup(html_text, 'lxml')
    # Get the last page
    try:
        pages = soup.find('ul', class_='pager-items')
        last_page = pages.find_all('li')[-1].text.replace('\n', '')
    except:
        last_page = 1
    return last_page

def get_website_apply(url):
    response = requests.get(url)
    website_apply = response.url
    return website_apply

def get_details_from_job(link_info):
    """
    Get the job details from the website in each page
    input: link_info
    Return: dictionary with the job details
    """
    # get request from the website
    html_text = requests.get(link_info).text
    # Using beautiful soup to parse the html
    soup = BeautifulSoup(html_text, 'lxml')
    #Get title jobs
    title = soup.find('h1', class_='govuk-heading-l').text.replace('  ', '').replace('\n', '')
    #Get website apply link
    link = soup.find('a', class_='govuk-button govuk-button--start').get('href')
    website_apply = get_website_apply(link)
    #Get description jobs
    description = soup.find('div', itemprop='description').get_text('\n').replace('\n\n\n\n',' \n ').replace('  ', '')

    #Get other data from rows
    rows = soup.find_all('tr', class_='govuk-table__row')
    list_th = []
    list_tr = []
    for row in rows:
        key = row.th.text.replace('  ', '').replace('\n', '').replace(':', '')
        info = row.td.text.replace('  ', '').replace('\n', '')
        list_th.append(key)
        list_tr.append(info)

    #Get the data from the rows
    posting_date,closing_date, company, location, salary, hours_shifts, type_contract,  reference = None ,None ,None ,None ,None ,None ,None ,None
    for i in range(len(list_th)):
        if list_th[i] == 'Closing date':
            closing_date = datetime.strptime(list_tr[i], '%d %B %Y').date()
        elif list_th[i] == 'Posting date':
            posting_date = datetime.strptime(list_tr[i], '%d %B %Y').date()
        elif list_th[i] == 'Company':
            company = list_tr[i]
        elif list_th[i] == 'Location':
            location = list_tr[i]
        elif list_th[i] == 'Salary':
            salary = list_tr[i]
        elif list_th[i] == 'Hours':
            hours_shifts = list_tr[i]
        elif list_th[i] == 'Job type':
            type_contract = list_tr[i]
        elif list_th[i] == 'Job reference':
            reference = list_tr[i]

    job_Details = create_dictionary(title, link_info, posting_date,closing_date, company, location, salary, hours_shifts, type_contract, website_apply, reference, description)
    return job_Details

def iterate_jobs_in_page(url):
    """
    Get the link job details from result search page
    input: url
    Return: list of dictionary job details
    """
    # Empty list to store the jobs details
    list_of_jobs_details = []
    # get request from the website
    html_text = requests.get(url).text
    # Empty list to store the jobs details
    list_of_jobs_details = []
    # Using beautiful soup to parse the html
    soup = BeautifulSoup(html_text, 'lxml')
    # Get lists of jobs
    jobs = soup.find_all('div', class_='search-result')
    # For loop to go through the jobs

    for job in jobs:
        # get title job
        link = job.find(
            'a', class_='govuk-link').get('href')
        job_details = get_details_from_job(link)
        list_of_jobs_details.append(job_details)
        print(f'{len(list_of_jobs_details)} jobs scraped')

    return list_of_jobs_details

def iterate_pages(url):
    """
    Loop through all the pages
    input:
    return: dataframe of jobs details
    """
    last_page = int(get_last_page(url))
    print(f'total pages: {last_page}')
    list_of_jobs_details = iterate_jobs_in_page(url)
    print('page: 1 done')
    for page in range(2, last_page + 1):
        new_url = f'{url}&page={page}'
        list_of_jobs_details += iterate_jobs_in_page(new_url)
        print(f'page: {page} done')
    print(f'Scrapping is done')
    return pd.DataFrame(list_of_jobs_details)

def main(url):
    list_jobs = iterate_pages(url)
    list_jobs.fillna('None', inplace=True)
    return list_jobs

