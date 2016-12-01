# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from Tkinter import *
import json
import re

# This script can be used to retrieve the USCIS case status.
# It's very boring to go to the USCIS website and enter the 13-digit case number
# and then get the status
# So I automated it. I make POST request to the uscis page with the case number,
# use beautiful soup to extract the required data and details, (optional) use the
# IFTTT maker channel to send the details about my case status to my phone via SMS

# This script can also be added in a cron job and have a raspberry pi run it periodically
# for eg. once every hour from 10 AM - 8 PM everyday to make our lives easier

# (optional) A receipe can also be created on IFTTT to send to send these details
#            to a Slack channel. For eg. If Maker then Slack

# case number should be a 13 digit number
case_number = 'ABC1234567890'

url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'

# I'm using the Maker channel from IFTTT to send an sms to my phone
# Steps:
# 1. Create a new trigger in the IFTTT maker channel. Name it for eg. "uscis_case_status"
# 2. Create a new IFTTT receipe - If MAKER then SMS. This will send an SMS to your phone
#    if a MAKER event is generated
# 3. Get your key for the maker event and replace the YOUR-KEY below with your key
maker_channel_url = 'https://maker.ifttt.com/trigger/uscis_case_status/with/key/YOUR-KEY'

# the body required for the POST request
body = {'changeLocale': '', 'appReceiptNum': case_number, 'initCaseSearch': 'CHECK+STATUS'}

# make the POST request
r = requests.post(url, verify=False, data=body)
print(r.status_code)

# create the soup from the HTML response
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup.prettify())
soup.prettify()

# find the header of the required content
my_status_header = soup.find("div", {"class": "rows text-center"}).h1.string

# find the paragraph of the requied content
my_status_p = soup.find("div", {"class": "rows text-center"}).p.get_text()

# print my_status header and paragraph
print(my_status_header)
print(my_status_p)

status_header = str(my_status_header)
status_paragraph = str(my_status_p)

# send to maker channel which will send an sms to your phone
payload = {'value1': status_header, 'value2': status_paragraph}
r = requests.post(maker_channel_url, json=payload)
print(r.status_code)
