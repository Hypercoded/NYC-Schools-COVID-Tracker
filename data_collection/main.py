# Structure


from data_collection.report_generation import generate_normal_report, generate_hybrid_report

# my men, i want you to know that these two functions
# have not been tested at all. i don't know if they work.
# however, it is 2am on a school day and i must sleep
# i wish you the best of luck, o7
generate_normal_report()

generate_hybrid_report()

#the only instructions ill leave back are:
# each one takes in the rawData json which is what u get when you call the api
# all you need to implement is something that gets every school from db.schools
# using .find({}) (note if u dont put anything in the brackets it will return everything which is what we want)
# and then for each school it will call the function that generates the report
# it will then store those reports somewhere, and then for each school it will
# update the key of the corresponding datapoint doc
# if u have a date thats "01-19-2022" that can be considered the key
# meaning datapointsCollection.update_one({
#                     "school_id": VARIABLEFORSCHOOLIDGOESHERE
#                 }, {"$set": {"01-19-2022": report}})
# where report is the generated report then it would work
# ur only goal is to figure out what the correct date is as currently we have to go into the rawData["updateDate"]
# copy that date, and cut off the hour second etc and just get the day and month and year itself
# so just do that, use it as the key, and then store the report in the datapoints collection using that set thing and ur
# https://www.w3schools.com/python/python_mongodb_update.asp

