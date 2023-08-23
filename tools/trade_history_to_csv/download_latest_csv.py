#!/bin/

# Libraries
from datetime import date
import csv
import os
import pandas as pd
import sys


import urllib.request
page = urllib.request.urlopen( 'https://www.tdameritrade.com/' )
print(page.read())

# tdlink = 'https://www.tdameritrade.com'
# todays_date = date.today()
# todays_date = str(todays_date).split( "-" )
# year = todays_date[0]
# user_name = input("User name: " )
# password = input("Password: " )

# print( "\n\n\n\n" + "User Input" )
# print( "-----------------------" )
# print( "Username: " + user_name )
# print( "Password: " + password )
# print( "Year: ", year)


