import os
from datetime import date
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel

from db_functions import engine as engine_db
from db_functions import get_days as get_days
from db_functions import jobs_available_count as jobs_available_count_db
from db_functions import jobs_count as jobs_count_db
from db_functions import last_posting_date as last_posting_date_db
from db_functions import read_available_jobs as read_available_jobs_db
from db_functions import read_from_db as read_from_db

load_dotenv()
app = FastAPI(title="API jobs from dwp")

# properties required during user creation
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
    last_posting_date: date
    jobs_count: int
    data: List[Jobs_details]

    class Config:
        schema_extra = {
            "example": [
                {
                    "last_posting_date": "2022-06-30",
                    "jobs_count": 3564,
                    "data": [
                        {
                            "title": "Software Engineer",
                            "posting_date": "2022-01-01",
                            "closing_date": "2022-01-05",
                            "salary": "£10,000 to £15,000",
                            "hours_shifts": "Full time",
                            "location": "London",
                            "company": "DWP",
                            "type_contract": "Permanent",
                            "Information": "Information about the job",
                            "Link_info": "www.dwp.gov.uk/details/12345",
                            "reference": "12345",
                            "website_apply": "www.company/apply/job/12345",
                        },
                        {
                            "title": "developer Engineer",
                            "posting_date": "2022-05-01",
                            "closing_date": "2022-05-04",
                            "salary": "£15,000 to £20,000",
                            "hours_shifts": "Full time",
                            "location": "London",
                            "company": "DWP",
                            "type_contract": "Permanent",
                            "Information": "Information about the job",
                            "Link_info": "www.dwp.gov.uk/details/6789",
                            "reference": "6789",
                            "website_apply": "www.company/apply/job/66789",
                        },
                    ],
                }
            ]
        }


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/jobs", response_model=response_data)
async def root():
    # Get connection to database
    credentials = os.getenv("DATABASE_URL")
    engine = engine_db(credentials)
    # read data from database
    data = read_from_db("jobs", engine)
    last_update = last_posting_date_db(engine)
    jobs_count = jobs_count_db(engine)
    response = response_data(
        last_posting_date=last_update,
        jobs_count=jobs_count,
        data=data,
    )
    return response


@app.get("/available_jobs", response_model=response_data)
async def root():
    # Get connection to database
    credentials = os.getenv("DATABASE_URL")
    engine = engine_db(credentials)
    # read data from database
    data = read_available_jobs_db("jobs", engine)
    last_update = last_posting_date_db(engine)
    jobs_count = jobs_available_count_db(engine)
    response = response_data(
        last_posting_date=last_update,
        jobs_count=jobs_count,
        data=data,
    )
    return response
