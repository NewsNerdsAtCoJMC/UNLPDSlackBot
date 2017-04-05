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



print("\nArrest Statistics:")
arrest_stats = soup.find("div", {"id": "ctl00_ContentPlaceHolder1_ArrestStatisticsSection"})
arrest_table = arrest_stats.find("table")

arrest_stats = []
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
    arrest_stats.append(stat_entry_dict)

# Save arrest stats to pickle file

pickle.dump( arrest_stats, open( "data/arrest_stats_ytd.p", "wb" ) )

#arrest_table.find_all('tr')[1:][0]
#import readline; print '\n'.join([str(readline.get_history_item(i)) for i in range(readline.get_current_history_length())])
#import readline
#for i in range(readline.get_current_history_length()):
#    print(readline.get_history_item(i + 1))
