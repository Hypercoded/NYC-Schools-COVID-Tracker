# Structure
import requests, json
from pymongo import MongoClient

PUBLIC_DIRECTORY = "https://schoolcovidreportcard.health.ny.gov/data/directory/public.directory.abbreviated.json"

connectionString = ""

# Connect to MongoDB
# client = MongoClient(connectionString)


# Temporary btw
schoolsSchema = {
    "school_name": "",
    "school_id": "",

    "district_name": "",
    "district_id": "",

    "total_students": "",
    "total_faculty": "",

    "covid_report": {  # This is only for "as of right now", historical data such as graphs will be stored in a
        # different collection
        "last_updated": "", ## maybe replace this with a datetime object

        "total_cases": "",

        "student_cases": "",
        "faculty_cases": "",



        "covid_report": {

            "total": {},

            "today": {},

            "yesterday": {},

            "this_week": {},

            "last_week": {},


        }



    },

}


def loadAllSchools():  # NOTE: NEVER EVER EVER CALL THIS IN PRODUCTION. ITS USED TO LOAD SCHOOLS INTO THE DATABASE.
    url = requests.get(PUBLIC_DIRECTORY)
    data = json.loads(url.text)
    print(len(data))
    # for k, v in data.items():
    #    print(k, v)
    ## key is the name of the school, we can use this for search results n stuff


loadAllSchools()
