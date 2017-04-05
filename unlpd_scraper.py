#!/usr/bin/python

# Import the needed modules
from selenium import webdriver
import datetime
from datetime import date
from datetime import datetime, timedelta, date
import sys
import time
import csv

# Lifted from http://stackoverflow.com/a/25166764
def datetime_range(start=None, end=None):
    span = end - start
    for i in range(span.days + 1):
        yield start + timedelta(days=i)

# Generate a list of datetime objects for scraper
start_date = date(2006,1,1)
end_date = datetime.now()

# The list of dates
date_list = []

#for crime_date in datetime_range(start=start_date, end=end_date):
#    date_list.append(crime_date)

#print("Dates:")

#for date in date_list:
#    print(date)

# Fire up a webbrowser in selenium
print("Starting Chrome...")
browser = webdriver.Chrome()
print("Going to https://scsapps.unl.edu/policereports/MainPage.aspx...")
browser.get("https://scsapps.unl.edu/policereports/MainPage.aspx")
print("Clicking on \"Advanced Search\"...")
browser.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_AdvancedSearchButton").click()

def getCrimeByDay(crime_datetime):
    browser = webdriver.Chrome()
    print("Going to https://scsapps.unl.edu/policereports/MainPage.aspx...")
    browser.get("https://scsapps.unl.edu/policereports/MainPage.aspx")
    print("Clicking on \"Advanced Search\"...")
    browser.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_AdvancedSearchButton").click()
