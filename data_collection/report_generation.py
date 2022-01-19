import datetime
import json


def generate_normal_report(rawData):
    template = open('templates/datapoint.json')
    datapointTemplate = json.load(template)
    results = datapointTemplate.copy()




    currentCounts = rawData["currentCounts"]
    lastUpdated = rawData["updateDate"]


    date = datetime.datetime.strptime(lastUpdated, "%b %d, %Y %X %p")
    lastUpdated_formatted = date.strftime("%Y-%m-%d")
    today_formatted = datetime.datetime.now().strftime("%Y-%m-%d")



    if today_formatted == lastUpdated_formatted:
        dataIsToday = True

    dataMap = {
        "timestamp": datetime.datetime.now(),

        "population": rawData["currentCounts"]["totalEnrolled"],

        "positiveCount": currentCounts["positiveTotal"],
        "positiveRate": int(currentCounts["positiveTotal"]) / int(rawData["currentCounts"]["totalEnrolled"]),

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
    template.close()

    results = datapointTemplate.copy()

    currentCounts = rawData["currentCounts"]
    lastUpdated = rawData["updateDate"]

    date = datetime.datetime.strptime(lastUpdated, "%b %d, %Y %X %p")
    lastUpdated_formatted = date.strftime("%m-%d-%y")
    today_formatted = datetime.datetime.now().strftime("%m-%d-%y")

    dataIsToday = False

    if today_formatted == lastUpdated_formatted:
        dataIsToday = True

    dataMap = {
        "timestamp": datetime.datetime.now(),

        "population": currentCounts["onSiteTotalPopulation"] + currentCounts["offSiteTotalPopulation"],

        "positiveCount": currentCounts["onSitePositiveTotal"] + currentCounts[
            "offSitePositiveTotal"],
        "positiveRate": int(currentCounts["onSitePositiveTotal"]) + int(
            currentCounts["offSitePositiveTotal"]) /  # again, literal spaghetti
                        currentCounts["onSiteTotalPopulation"] + currentCounts[
                            "offSiteTotalPopulation"],

        "positiveStudents": currentCounts["offSitePositiveStudents"] + currentCounts[
            "onSitePositiveStudents"],
        "positiveTeachers": currentCounts["onSitePositiveTeachers"] + currentCounts["onSitePositiveStaff"] +
                            currentCounts["offSitePositiveTeachers"] + currentCounts[
                                "offSitePositiveStaff"],

        "legacyData": False,
        "dataReported": dataIsToday

    }

    for key, data in dataMap.items():
        results[key] = data
    return results
