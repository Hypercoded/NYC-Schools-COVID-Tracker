# Structure
import requests
import pymongo
import datetime

connectionString = "no"

client = pymongo.MongoClient(connectionString)

schoolsCollection = client.db.schools
datapointsCollection = client.db.datapoints

from report_generation import generate_normal_report, generate_hybrid_report


def logSchools():
    for school in schoolsCollection.find({}):

        overwrite = True

        try:
            data = requests.get(
                f"https://schoolcovidreportcard.health.ny.gov/data/public/school.{school['district_id']}.{school['school_id']}.json").json()
            lastUploadedDate = datetime.datetime.strptime(data["updateDate"], "%b %d, %Y %X %p")
            formattedDate = lastUploadedDate.strftime("%m-%d-%y")
            if formattedDate in datapointsCollection.find({"school_id": school["school_id"]}) or overwrite:

                print("Generating report for: " + school["school_name"])

                if "studentEnrolled" in data["currentCounts"]:
                    report = generate_normal_report(data)
                else:
                    report = generate_hybrid_report(data)

                # TODO: dont count data if the last updated date was already
                datapointsCollection.update_one(
                    {"school_id": school["school_id"]},
                    {"$set": {formattedDate: report}}
                )
            else:
                print("School already added: " + school["school_name"])
        except:
            print("error loading school " + school["school_id"])


logSchools()

#TODO:
# 1. Create a collection in mongodb for when we query data, it should be a statistics/utility collection.
# 2. Everytime you generate a report in report_generation.py, you should set the dataSourceDate attribute of the school
# inside the collection to the updateDate value. That way we know what day the latest data was sourced from.
# We can skip schools that have data sourced from the current, new "updateDate" value.
