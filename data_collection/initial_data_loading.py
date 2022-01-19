import datetime
import json
from pymongo import MongoClient
import requests


PUBLIC_DIRECTORY = "https://schoolcovidreportcard.health.ny.gov/data/directory/public.directory.abbreviated.json"

connectionString = "no"

# Connect to MongoDB
client = MongoClient(connectionString)

schoolsCollection = client.db.schools
datapointsCollection = client.db.datapoints
districtsCollection = client.db.districts

apiData = requests.get(PUBLIC_DIRECTORY).json()

def load_schools():
    res = []
    with open('templates/school.json') as template:

        schoolTemplate = json.load(template)

        for name, schoolInfo in apiData.items():

            try:
                if schoolInfo["type"] == "District": continue

                url = f"https://schoolcovidreportcard.health.ny.gov/data/public/school.{schoolInfo['districtBedsCode']}.{schoolInfo['schoolBedsCode']}.json"
                rawData = requests.get(url).json()

                hybridLearning = "onSiteStudentPopulation" in rawData["currentCounts"]

                newSchool = schoolTemplate.copy()

                if not hybridLearning:
                    newSchool = create_normal_school(newSchool, rawData)

                else:
                    newSchool = create_hybrid_school(newSchool, rawData)

                schoolsCollection.insert_one(newSchool)

                newDatapointParent = newSchool.copy()
                newDatapointParent.pop("covid_report")
                newDatapointParent.pop("geography")

                newDatapointParent["last_updated"] = datetime.datetime.now()

                datapointsCollection.insert_one(newDatapointParent)

                datapointsCollection.update_one({
                    "school_id": schoolInfo["schoolBedsCode"]
                }, {"$set": create_normal_historical_report(rawData)})

                res.append(newSchool)
                print("School: (" + name + ") added to database.")
            except:
                print("School: (" + name + ") failed to add to database.")



    return res


def create_normal_school(schoolJSON, rawData):
    new = schoolJSON.copy()
    dataMap = {
        "school_name": rawData["name"],
        "school_id": rawData["bedsCode"],
        "district_name": rawData["districtName"],
        "district_id": rawData["districtBedsCode"],
        "geography": {
            "zip": rawData["zip"],
            "address": rawData["addressLine1"],
            "city": rawData["city"]
        },
        "total_students": int(rawData["studentEnrolled"]),
        "total_faculty": int(rawData["teacherEnrolled"]) + int(rawData["staffEnrolled"]),
        "total_population": int(rawData["studentEnrolled"]) + int(rawData["teacherEnrolled"]) + int(
            rawData["staffEnrolled"]),


    }

    for key, data in dataMap.items():
        new[key] = data

    return new


def create_hybrid_school(schoolJSON, rawData):
    new = schoolJSON.copy()
    dataMap = {
        "school_name": rawData["name"],
        "school_id": rawData["bedsCode"],
        "district_name": rawData["districtName"],
        "district_id": rawData["districtBedsCode"],
        "geography": {
            "zip": rawData["zip"],
            "address": rawData["addressLine1"],
            "city": rawData["city"]
        },
        "total_students": int(rawData["currentCounts"]["onSiteStudentPopulation"]) + int(
            rawData["currentCounts"]["offSiteStudentPopulation"]),
        "total_faculty": int(rawData["currentCounts"]["onSiteTeacherPopulation"]) + int(
            rawData["currentCounts"]["onSiteStaffPopulation"]),
        "total_population": int(rawData["currentCounts"]["onSiteTotalPopulation"]) + int(
            rawData["currentCounts"]["offSiteTotalPopulation"])
    }

    for key, data in dataMap.items():
        new[key] = data

    return new


def create_district(districtJSON, rawDistrictData):
    new = districtJSON.copy()
    dataMap = {

        "district_name": rawDistrictData["name"],
        "district_id": rawDistrictData["bedsCode"],

        "total_students": int(rawDistrictData["currentCounts"]["studentEnrolled"]),
        "total_faculty": int(rawDistrictData["currentCounts"]["teacherEnrolled"]) + int(
            rawDistrictData["currentCounts"]["staffEnrolled"]),
        "total_population": int(rawDistrictData["currentCounts"]["studentEnrolled"]) + int(
            rawDistrictData["currentCounts"]["teacherEnrolled"]) + int(
            rawDistrictData["currentCounts"]["staffEnrolled"]),
        # messier than my hairline
        # - jordan
    }

    for key, data in dataMap.items():
        new[key] = data

    newDatapointParent = new.copy()
    newDatapointParent.pop("covid_report")
    newDatapointParent["last_updated"] = datetime.datetime.now()

    datapointsCollection.insert_one(newDatapointParent)

    districtsCollection.insert_one(new)
    return new


def create_normal_historical_report(rawData, limit=None):
    with open('templates/datapoint.json') as template:
        datapointTemplate = json.load(template)

        results = {}

        for caseHistory in rawData["positiveHistory"]:
            newDatapoint = datapointTemplate.copy()
            date = caseHistory["date"]

            date = date.replace(",", "")

            try:
                strdate = ", ".join(date.split(" ")[:3])
                date = datetime.datetime.strptime(strdate, "%b, %d, %Y")
                formattedDate = date.strftime("%m-%d-%y")
            except:
                date = datetime.datetime.now()
                datetimeFailed = True
                print("Failed to parse date: " + date)
                formattedDate = date.strftime("%m-%d-%y")

            # screeningHistory = rawData["totalScreeningTests"][date]


            dataMap = {
                "timestamp": date,

                "population": rawData["currentCounts"]["totalEnrolled"],
                "positiveCount": caseHistory["positiveCount"],
                "positiveRate": int(caseHistory["positiveCount"]) / int(rawData["currentCounts"]["totalEnrolled"]),

                "legacyData": True,
                # Legacy Data refers to data that was pulled from historical reports instead of our own data collection
                # They leave out various pieces of info, most notable discernment between student & teacher cases
                # and also the amount of positives from screening.

            }

            for key, data in dataMap.items():
                newDatapoint[key] = data
            results[formattedDate] = newDatapoint
        return results


def create_hybrid_historical_report(rawData, limit=None):
    with open('templates/datapoint.json') as template:
        datapointTemplate = json.load(template)

        results = {}

        for caseHistory in rawData["positiveHistory"]:

            newDatapoint = datapointTemplate.copy()
            date = caseHistory["date"]
            datetimeFailed = False
            date = date.replace(",", "")
            try:
                strdate = ", ".join(date.split(" ")[:3])
                date = datetime.datetime.strptime(strdate, "%b, %d, %Y")
                formattedDate = date.strftime("%m-%d-%y")
            except:
                date = datetime.datetime.now()
                datetimeFailed = True
                print("Failed to parse date: " + date)
                formattedDate = date.strftime("%m-%d-%y")

            dataMap = {
                "timestamp": date,

                "population": int(rawData["currentCounts"]["onSiteTotalPopulation"]) + int(
                    rawData["currentCounts"]["offSiteTotalPopulation"]),
                "positiveCount": caseHistory["positiveCount"],
                "positiveRate": caseHistory["positiveCount"] / (
                        int(rawData["currentCounts"]["onSiteTotalPopulation"]) + int(
                    rawData["currentCounts"]["offSiteTotalPopulation"])),

                "legacyData": False,
                # Legacy Data refers to data that was pulled from historical reports instead of our own data collection
                # They leave out various pieces of info, most notable discernment between student & teacher cases
                # and also the amount of positives from screening.

                ## WHY DO I FEEL LIKE A 1ST GRADER LEARNING ENGLISH
                ## WHENEVER I USE PYTHON TERNARY OPERATORS
            }

            for key, data in dataMap.items():
                newDatapoint[key] = data
            results[formattedDate] = newDatapoint
        return results


def load_districts():
    districtsList = []
    with open('templates/district.json') as template:
        template = json.load(template)

        for k, v in apiData.items():

            if v["type"] == "District":
                print("District: (" + k + ") added to database.")
                # print(create_district(template, requests.get(f"https://schoolcovidreportcard.health.ny.gov/data/public/district.{v['districtBedsCode']}.json").json()))
                districtsList.append(create_district(template, requests.get(
                    f"https://schoolcovidreportcard.health.ny.gov/data/public/district.{v['districtBedsCode']}.json").json()))

    return districtsList

load_schools()

load_districts()
