# Structure
import requests
import pymongo
import datetime
import json

connectionString = ""

client = pymongo.MongoClient(connectionString)

schoolsCollection = client.db.schools
datapointsCollection = client.db.datapoints
internalCollection = client.db.internal

from report_generation import generate_normal_report, generate_hybrid_report


def generateSummary(datapoints):
    file = open('templates/school.json', 'r')
    schoolDoc = json.load(file)
    file.close()

    template = schoolDoc.pop("covid_report")


    #TODO: do the math n stuff that summarizes the data idk
    #TODO: williams do the stuff here

    template["total"] = {

    }

    return template




def logSchools():
    for school in schoolsCollection.find({}):

        try:
            data = requests.get(
                f"https://schoolcovidreportcard.health.ny.gov/data/public/school.{school['district_id']}.{school['school_id']}.json").json()
            lastUploadedDate = datetime.datetime.strptime(data["updateDate"], "%b %d, %Y %X %p")
            formattedDate = lastUploadedDate.strftime("%m-%d-%y")
            if not "dataSourceDate" in school or not formattedDate == school["dataSourceDate"]:

                print("Generating report for: " + school["school_name"])

                if "studentEnrolled" in data["currentCounts"]:
                    report = generate_normal_report(data)
                else:
                    report = generate_hybrid_report(data)

                popularityDoc = {
                    "discord_command_usage": 0,
                    "cum_member_count": 0,
                    "cum_server_count": 0,
                    "cum_ping_subscribed": 0,
                }  # temp since i need to add it to the "schema" also cum means cumulative.

                # TODO: dont count data if the last updated date was already
                datapointsCollection.update_one(
                    {"school_id": school["school_id"]},
                    {"$set": {formattedDate: report}}
                )

                newCovidReport = generateSummary(report)

                schoolsCollection.update_one(
                    {"school_id": school["school_id"]},
                    {"$set": {"dataSourceDate": formattedDate, "popularity": popularityDoc, "covid_report": newCovidReport}}
                )
            else:
                print("School already added: " + school["school_name"])
        except:
            print("Error with: " + school["school_name"])


logSchools()

#TODO: instead of querying db each time just get one long fetch at the beginning

#TODO: remove 01-19-22 data points from the db
