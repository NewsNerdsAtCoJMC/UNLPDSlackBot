#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import sys
import re
import pickle


print("Bleep Bloop, UNLPD Year-to-Date Scraper Started!")

results = requests.get("https://scsapps.unl.edu/PoliceReports/ClerySummaryReport.aspx")

if results.status_code != 200:
    print("Request didn't return 200, killing script.")
    sys.exit()


c = results.content


soup = BeautifulSoup(c, "lxml")

print("\nCrime Statistics:")
crime_stats = soup.find("div", {"id": "ctl00_ContentPlaceHolder1_CrimeStatisticsSection"})
crime_table = crime_stats.find("table")

# Stats table that will be saved to pickle file
crime_stats_out = []
for entry in crime_table.find_all("tr", id=re.compile('SubCategoryRow$')):
    #print(entry)
    stat_entry_dict = {}
    sub_category = entry.find("span", id=re.compile('SubCategory$')).text
    on_campus = entry.find("span", id=re.compile('OnCampus$')).text
    on_campus_housing = entry.find("span", id=re.compile('Housing$')).text
    non_campus = entry.find("span", id=re.compile('NonCampus$')).text
    public_property = entry.find("span", id=re.compile('PublicProperty$')).text

    stat_entry_dict["sub_category"] = sub_category.replace(":", "")
    stat_entry_dict["on_campus"] = int(on_campus)
    stat_entry_dict["on_campus_housing"] = int(on_campus_housing)
    stat_entry_dict["non_campus"] = int(non_campus)
    stat_entry_dict["public_property"] = int(public_property)

    print("\nSub-Category: {}".format(stat_entry_dict["sub_category"]))
    print("On Campus: {}".format(stat_entry_dict["on_campus"]))
    print("On Campus Housing: {}".format(stat_entry_dict["on_campus_housing"]))
    print("Non Campus: {}".format(stat_entry_dict["non_campus"]))
    print("Public Property: {}".format(stat_entry_dict["public_property"]))
    # Append to stats table
    crime_stats_out.append(stat_entry_dict)

# Save arrest stats to pickle file
pickle.dump(crime_stats_out, open("data/crime_stats_ytd.p", "wb"))

print("\nArrest Statistics:")
arrest_stats = soup.find("div", {"id": "ctl00_ContentPlaceHolder1_ArrestStatisticsSection"})
arrest_table = arrest_stats.find("table")

# Stats table that will be saved to pickle file
arrest_stats_out = []
for entry in arrest_table.find_all("tr")[1:]:
    stat_entry_dict = {}
    sub_category = entry.find("span", id=re.compile('SubCategory$')).text
    on_campus = entry.find("span", id=re.compile('OnCampus$')).text
    on_campus_housing = entry.find("span", id=re.compile('Housing$')).text
    non_campus = entry.find("span", id=re.compile('NonCampus$')).text
    public_property = entry.find("span", id=re.compile('PublicProperty$')).text

    stat_entry_dict["sub_category"] = sub_category
    stat_entry_dict["on_campus"] = int(on_campus)
    stat_entry_dict["on_campus_housing"] = int(on_campus_housing)
    stat_entry_dict["non_campus"] = int(non_campus)
    stat_entry_dict["public_property"] = int(public_property)

    print("\nSub-Category: {}".format(stat_entry_dict["sub_category"]))
    print("On Campus: {}".format(stat_entry_dict["on_campus"]))
    print("On Campus Housing: {}".format(stat_entry_dict["on_campus_housing"]))
    print("Non Campus: {}".format(stat_entry_dict["non_campus"]))
    print("Public Property: {}".format(stat_entry_dict["public_property"]))

    # Append to stats table
    arrest_stats_out.append(stat_entry_dict)

# Save arrest stats to pickle file
pickle.dump(arrest_stats_out, open("data/arrest_stats_ytd.p", "wb"))

print("\nReported Hate Crimes:")
hate_crimes = soup.find("div", {"id": "ctl00_ContentPlaceHolder1_HateCrimesSection"})
# arrest_table = arrest_stats.find_all("div")

# Stats table that will be saved to pickle file
hate_crimes_out = []

hate_crimes = hate_crimes.find_all("span")

hate_crimes_split = [hate_crimes[x:x+4] for x in range(0, len(hate_crimes),4)]

for entry in hate_crimes_split:

    joined_entry = "".join(str(item) for item in entry)

    searchable = BeautifulSoup(joined_entry, "lxml")

    stat_entry_dict = {}

    category = searchable.find("span", id=re.compile('Category$')).text
    bias = searchable.find("span", id=re.compile('Bias$')).text
    count = searchable.find("span", id=re.compile('Count$')).text

    stat_entry_dict["category"] = category
    stat_entry_dict["bias"] = bias
    stat_entry_dict["count"] = int(count)

    print("\nCategory: {}".format(stat_entry_dict["category"]))
    print("Bias: {}".format(stat_entry_dict["bias"]))
    print("Count: {}".format(stat_entry_dict["count"]))


    # Append to stats table
    hate_crimes_out.append(stat_entry_dict)

# Save hate crimes to pickle file
pickle.dump(hate_crimes_out, open("data/hate_crimes_ytd.p", "wb"))

print("\nOn-Campus Fire Statistics:")
fire_stats = soup.find("div", {"id": "ctl00_ContentPlaceHolder1_FireStatisticsSection"})
fire_table = fire_stats.find("table")

# Stats table that will be saved to pickle file
fire_stats_out = []
for entry in fire_table.find_all("tr")[1:]:

    stat_entry_dict = {}
    location = entry.find("span", id=re.compile('BuildingName_Address$')).text
    fire_count = entry.find("span", id=re.compile('FireCount$')).text
    fire_number = entry.find("span", id=re.compile('FireNumber$')).text
    fire_type_cause = entry.find("span", id=re.compile('FireType_CauseOfFire$')).text
    injury_count = entry.find("span", id=re.compile('NumberOfInjuries$')).text
    death_count = entry.find("span", id=re.compile('NumberOfDeaths$')).text
    property_damage = entry.find("span", id=re.compile('PropertyDamage$')).text


    stat_entry_dict["location"] = location
    stat_entry_dict["fire_count"] = int(fire_count)
    stat_entry_dict["fire_number"] = int(fire_number)
    stat_entry_dict["fire_type_cause"] = fire_type_cause
    stat_entry_dict["injury_count"] = int(injury_count)
    stat_entry_dict["death_count"] = int(death_count)


    print("\n")
    for key, value in stat_entry_dict.items():
        print("{}: {}".format(key, value))
    # Append to stats table
    fire_stats_out.append(stat_entry_dict)

# Save arrest stats to pickle file
pickle.dump(fire_stats_out, open("data/fire_stats_ytd.p", "wb"))
