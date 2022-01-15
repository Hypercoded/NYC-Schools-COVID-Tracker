# NYC Schools COVID Tracker

This is a small project meant for the purpose of aggregating COVID data pulled from the state's official school covid data.


# How does it work?

Every day we poll the COVID case data for numerous schools in the NYC region on the [School Health Report Card](https://schoolcovidreportcard.health.ny.gov/) website, provided by the state.

We also will have a Discord Bot and Twitter Account that you can  receive alerts from, allowing you to get the info as soon as possible.

Another goal is to have a website that provides a detailed rundown of each school in a list, meaning there's no need for you to manually check each school.

# Why does this exist?

We feel as if the provided website is lackluster and hard to check for a daily update on schools near you. Creating this allows us to get updates in a school server without having to manually check for the data.

# What programming lanugages/frameworks?

We'll use [MongoDB] (https://www.mongodb.com/) for data storage. We're using [PyCord](https://github.com/Pycord-Development/pycord) as a framework for our discord bots. Twitter bot will use [Tweepy](https://www.tweepy.org/), and the website will run off [NextJS](https://nextjs.org/).

