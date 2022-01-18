import datetime
import json


def generate_normal_report(rawData):
    template = open('templates/datapoint.json')
    datapointTemplate = json.load(template)

    results = datapointTemplate.copy()

    currentCounts = rawData["currentCounts"]
    lastUpdated = rawData["updateDate"]

    try:
        date = datetime.datetime.strptime(lastUpdated, "%b %d, %Y %X %p")
    except:
        date = datetime.datetime.now()
        print("Failed to parse date: " + date)

    dataMap = {
        "date": date,
        "timestamp": datetime.datetime.now(),

        "population": currentCounts["totalEnrolled"],

        "positiveCount": currentCounts["positiveTotal"],
        "positiveRate": int(currentCounts["positiveTotal"]) / int(currentCounts["totalEnrolled"]),

        "positiveStudents": currentCounts["positiveStudents"],
        "positiveTeachers": currentCounts["positiveTeachers"] + currentCounts["positiveStaff"],

        "legacyData": False,

    }

    for key, data in dataMap.items():
        results[key] = data

    return results


def generate_hybrid_report(rawData):
    template = open('templates/datapoint.json')
    datapointTemplate = json.load(template)

    results = datapointTemplate.copy()

    currentCounts = rawData["currentCounts"]
    lastUpdated = rawData["updateDate"]

    try:
        date = datetime.datetime.strptime(lastUpdated, "%b %d, %Y %X %p")
    except:
        date = datetime.datetime.now()
        print("Failed to parse date: " + date)

    dataMap = {
        "date": date,
        "timestamp": datetime.datetime.now(),

        "population": currentCounts["onSiteTotalPopulation"] + currentCounts["offSiteTotalPopulation"],

        "positiveCount": currentCounts["onSitePositiveTotal"] + currentCounts["offSitePositiveTotal"],
        "positiveRate": int(currentCounts["onSitePositiveTotal"]) + int(currentCounts["offSitePositiveTotal"]) / # again, literal spaghetti
                        currentCounts["onSiteTotalPopulation"] + currentCounts["offSiteTotalPopulation"],

        "positiveStudents": currentCounts["offSitePositiveStudents"] + currentCounts["onSitePositiveStudents"],
        "positiveTeachers": currentCounts["onSitePositiveTeachers"] + currentCounts["onSitePositiveStaff"] +
                            currentCounts["offSitePositiveTeachers"] + currentCounts["offSitePositiveStaff"],

        "legacyData": False,

    }

    for key, data in dataMap.items():
        results[key] = data

    return results