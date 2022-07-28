#%%
from datetime import date
from fastapi import FastAPI
from db_functions import engine as engine_db
from db_functions import read_from_db as read_from_db
from db_functions import get_days as get_days
from pydantic import BaseModel
from typing import List

app = FastAPI()



#properties required during user creation
class Jobs_details(BaseModel):
    title: str
    posting_date: date
    closing_date: date
    company: str
    location: str
    salary: str
    type_contract: str
    link_info: str
    website_apply: str
    hours_shifts: str
    description: str
    reference: str

class response_data(BaseModel):
    data : List[Jobs_details]

    class Config:
       schema_extra = {
            "example": [{
                "title": "Software Engineer",
                "posting_date": "2020-01-01",
                "closing_date": "2020-01-01",
                "salary": "£10,000 to £15,000",
                "hours_shifts": "Full time",
                "location": "London",
                "company": "DWP",
                "type_contract": "Permanent",
                "Information": "Information about the job",
                "Link_info": "www.dwp.gov.uk/details/12345",
                "reference": "12345",
                "website_apply": "www.company/apply/job/12345"
            }]
        }



@app.get("/", response_model = response_data)
async def root():
    # Get connection to database
    engine = engine_db()
    # read data from database
    df = read_from_db('jobs',engine)
    data = df.to_dict(orient='records')
    response = response_data(data=data)
    return response



