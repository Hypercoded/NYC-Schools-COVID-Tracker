# Structure
import requests
import pymongo
import datetime
connectionString = "no"

client = pymongo.MongoClient(connectionString)

schoolsCollection = client.db.schools
datapointsCollection = client.db.datapoints

from report_generation import generate_normal_report, generate_hybrid_report

schoolsToLog = [
    {"school_id": "342800011687", "district_id": "300000"},
    {"school_id": "342500011525", "district_id": "300000"},
    {"school_id": "321000011445", "district_id": "300000"},
]
def logSchools():
    for school in schoolsToLog:
        if True: #TODO: switch to try catch
            data = requests.get(f"https://schoolcovidreportcard.health.ny.gov/data/public/school.{school['district_id']}.{school['school_id']}.json").json()
            if "studentEnrolled" in data["currentCounts"]:
                report = generate_normal_report(data)
            else:
                report = generate_hybrid_report(data)

            formattedDate = datetime.datetime.now().strftime("%m-%d-%y")
            #TODO: dont count data if the last updated date was already
            print("test")
            datapointsCollection.update_one(
                {"school_id": school["school_id"]},
                {"$set": {formattedDate: report}}
            )
logSchools()


