# Overview:
#   This tool is meant to scan a list of stocks and return certain values. The 
#   requirements for this file can be found in the same file path, but labeled
#   requirements.

# TODO: initial revision was copied from here: https://github.com/pattertj/TDA-Trade-Scripts/blob/main/main.py
#       Need to refine calls and make it unique to my use case. 

import math
import os
import pprint
import chromedriver_autoinstaller
import datetime as dt
import httpx
import time

from dotenv import load_dotenv
from td.client import TDClient


##########################################################
# Sample env vars
##########################################################
# CHANGE THIS FILE NAME TO ".ENV"
# API_KEY='COPY FROM YOUR TDA DEVELOPER ACCOUNT APP'
# REDIRECT_URI = 'COPY FROM YOUR TDA DEVELOPER ACCOUNT APP'
#
# SYMBOL = '$SPX.X'
# TARGET_DTE = 30
# TRADE_TYPE = "1.1.2"
# OTM_PRICE_TARGET = 10.0
# SPREAD_PRICE_TARGET = 6.0
# SPREAD_WIDTH_TARGET = 30
##########################################################
# symbol = os.getenv('SYMBOL')
# target_dte = int(os.getenv('TARGET_DTE'))
# trade_type = (os.getenv('TRADE_TYPE'))
# otm_price_target = float(os.getenv('OTM_PRICE_TARGET'))
# otm_percent_target = float(os.getenv('MIN_OTM_PERCENT'))
# spread_price_target = float(os.getenv('SPREAD_PRICE_TARGET'))
# spread_width_target = float(os.getenv('SPREAD_WIDTH_TARGET'))
##########################################################

# Trade Settings
symbol = "$AAPL"
target_dte = 7
trade_type = '1.1.2'
otm_price_target = 10.0
otm_percent_target = 6
spread_price_target = 1
spread_width_target = 30

# Global Variables
G_TOKEN=os.getenv('TOKEN_PATH')

# Retrieves a list of stocks from a text file and returns it as a list
def GetInputStocks():

    # TODO: Hard coding needs to be replaced with environment variables
    # Paths / locations 
    REPO_PATH = "/Users/phoot/bin/code/trading"
    THIS_PATH = str(REPO_PATH) + "/tools/options-value-scan"
    THIS_NAME = os.path.basename(__file__)
    INPUT_NAME="list-1.txt"
    INPUT_PATH= str(REPO_PATH) + "/input/" + str( INPUT_NAME )


    # Take in input, put it into a list
    print( "\n\n" )
    if os.path.isfile( INPUT_PATH ):
        print( "'" + str(INPUT_PATH) + "' was selected." )
    else:
        print( "'" + str( INPUT_PATH ) + "' does not exist. Exiting." )
        exit()
    print("\n\n")

    file = open( INPUT_PATH, mode = 'r', encoding = 'utf-8-sig')
    stock_list = file.readlines()
    file.close()

    stocks = []
    for entry in stock_list:
        # TODO: function to check stocks for validity
        stocks.append( entry.replace("\n", "") )

    return stocks


def CreateClient():
    client = TDClient( client_id=os.getenv('CONSUMER_KEY'), 
                       redirect_uri=os.getenv('REDIRECT_URI'),
                       credentials_path='CREDNTIALS_PATH')
    #client = TDClient( client_id=str(os.getenv('CONSUMER_KEY')), 
    #                   redirect_uri=str(os.getenv('REDIRECT_URI')) )
    #                   json_path=str(os.getenv('JSON_PATH')) )

    client.login()

    return client







# Driver of the code
def main():
    # TODO: Add a func / feature to have user input for path, and if not use default. 
    # Set Up
    client = CreateClient()

    stocks = GetInputStocks()
    quotes = client.get_quotes(instruments=stocks)

    # pprint.pprint( quotes )


    # account_req = ["positions", "orders"]
    # accounts = client.get_accounts( account="all", fields=account_req )
    # pprint.pprint( accounts )

    # Might not work if not during trading hours. 
    try: 
        option_chain = client.get_options_chain( 'TSLA')
    except:
        current_time = time.ctime()
        print("Error getting option chain. Current time: " + str(current_time))
        option_chain = None
    pprint.pprint(option_chain)

    return



if __name__=="__main__":
    main()


