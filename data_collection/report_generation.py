import datetime
import json


def generate_normal_report(rawData):
    template = open('templates/datapoint.json')
    datapointTemplate = json.load(template)

    results = datapointTemplate.copy()

    todayCounts = rawData["todayCounts"]
    lastUpdated = rawData["updateDate"]

    try:
        date = datetime.datetime.strptime(lastUpdated, "%b %d, %Y %X %p")
    except:
        date = datetime.datetime.now()
        print("Failed to parse date: " + date)

    lastUpdated_formatted = date.strftime("%Y-%m-%d")
    today_formatted = datetime.datetime.now().strftime("%Y-%m-%d")

    dataIsToday = False

    if today_formatted == lastUpdated_formatted:
        dataIsToday = True

    dataMap = {
        "timestamp": datetime.datetime.now(),

        "population": rawData["currentCounts"]["totalEnrolled"],

        "positiveCount": todayCounts["positiveTotal"] if not dataIsToday else 0,
        "positiveRate": int(todayCounts["positiveTotal"]) / int(rawData["currentCounts"]["totalEnrolled"]) if not dataIsToday else 0,

        "positiveStudents": todayCounts["positiveStudents"] if not dataIsToday else 0,
        "positiveTeachers": todayCounts["positiveTeachers"] + todayCounts["positiveStaff"] if not dataIsToday else 0,

        "legacyData": False,

    }

    for key, data in dataMap.items():
        results[key] = data

    return results


def generate_hybrid_report(rawData):
    template = open('templates/datapoint.json')
    datapointTemplate = json.load(template)

    results = datapointTemplate.copy()

    todayCounts = rawData["todayCounts"]
    lastUpdated = rawData["updateDate"]

    try:
        date = datetime.datetime.strptime(lastUpdated, "%b %d, %Y %X %p")
    except:
        date = datetime.datetime.now()
        print("Failed to parse date: " + date)

    lastUpdated_formatted = date.strftime("%m-%d-%y")
    today_formatted = datetime.datetime.now().strftime("%m-%d-%y")

    dataIsToday = False

    if today_formatted == lastUpdated_formatted:
        dataIsToday = True

    dataMap = {
        "timestamp": datetime.datetime.now(),

        "population": todayCounts["onSiteTotalPopulation"] + todayCounts["offSiteTotalPopulation"],

        "positiveCount": todayCounts["onSitePositiveTotal"] + todayCounts[
            "offSitePositiveTotal"] if not dataIsToday else 0,
        "positiveRate": int(todayCounts["onSitePositiveTotal"]) + int(
            todayCounts["offSitePositiveTotal"]) /  # again, literal spaghetti
                        todayCounts["onSiteTotalPopulation"] + todayCounts[
                            "offSiteTotalPopulation"] if not dataIsToday else 0,

        "positiveStudents": todayCounts["offSitePositiveStudents"] + todayCounts[
            "onSitePositiveStudents"] if not dataIsToday else 0,
        "positiveTeachers": todayCounts["onSitePositiveTeachers"] + todayCounts["onSitePositiveStaff"] +
                            todayCounts["offSitePositiveTeachers"] + todayCounts[
                                "offSitePositiveStaff"] if not dataIsToday else 0,

        "legacyData": False,

    }

    for key, data in dataMap.items():
        results[key] = data

    return results
