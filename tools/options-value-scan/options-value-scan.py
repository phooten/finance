# Overview:
#   This tool is meant to scan a list of stocks and return certain values. The 
#   requirements for this file can be found in the same file path, but labeled
#   requirements.

#         # https://tda-api.readthedocs.io/en/latest/client.html#option-chain
# TODO: initial revision was copied from here: https://github.com/pattertj/TDA-Trade-Scripts/blob/main/main.py
#       Need to refine calls and make it unique to my use case. 

import math
import os
import pprint
import chromedriver_autoinstaller
import datetime as dt
import httpx
import time
import json

from datetime import datetime, timedelta
from dotenv import load_dotenv
# from td.client import TDClient
from tda import auth, client


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
load_dotenv()
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
    try:
        print("Token_path = " + str(os.getenv("TOKEN_PATH")))
        print("repo_path = " + str(os.getenv("REPO_PATH")))
        c = auth.client_from_token_file( str(os.getenv("TOKEN_PATH")), 
                                         str(os.getenv("CONSUMER_KEY")))
    # except FileNotFoundError:
    except:
        from selenium import webdriver
        with webdriver.Chrome() as driver:
            print("Token_path = " + str(os.getenv("TOKEN_PATH")))
            print("repo_path = " + str(os.getenv("REPO_PATH")))
            c = auth.client_from_login_flow( driver, 
                                             api_key=str(os.getenv("CONSUMER_KEY")),
                                             redirect_url=str(os.getenv("REDIRECT_URI")),
                                             token_path=str(os.getenv("TOKEN_PATH")) )

    return c

# Starting just puts for now. 
def scan_options( client, stocks, quotes, dte):


    for curr in stocks:
        print( "---------------------------------------------------")
        print( "Stock:\t\t" + str(curr))
        last_price = quotes[str(curr)]["regularMarketLastPrice"]
        print( "Last Price:\t$ " + str(last_price) )
        last_price = int(str(round(last_price)))
        
        # Might not work if not during trading hours. 
        # if str(curr) == "AMD":
            # op_chain = client.get_options_chain( 
            #                 option_chain={ 'symbol':str(curr),
            #                                'contract_type':TDClient. })
                                        #    'days_to_expiration':7,
                                        #    'strike_count':1,
                                        #    'strike_range':"OTM" } )
            # pprint.pprint( op_chain )
        #try: 
        #    option_chain = client.get_option_chain( curr, days_to_expiration=3 )
        #except:
        #    current_time = time.ctime()
        #    print("Error getting option chain. Current time: " + str(current_time))
        #    option_chain = None
        #print("Options Chain: \n\t" + str(option_chain))
        

        # 1. Get the strike prices at 1 week exp

        # 2. Go through each stock price from OTM to 90%
        #strike_interval = str(option_chain['interval'])
        #for strike in range( last_price, strike_interval):
        #    value = option_chain['MarkPrice'] / strike
        #    if value > 1:
        #        print( "VALUE FOUND.")
        #    else:
        #        print( "VALUE NOT FOUND.")
            # days_to_expiration
            # option_type
            # to_date
        
        
        # 3. Check the Value betwen each stock
        # 4. Print out Strike Prices with value

    return



# Driver of the code
def main():
    # TODO: Add a func / feature to have user input for path, and if not use default. 
    # Set Up
    client = CreateClient()

    stocks = GetInputStocks()
    quotes = client.get_quotes(stocks)
    print(json.dumps(quotes.json(), indent=4 ))
    
    dte = ( datetime.today() + timedelta(days=7) ).date()
    print("Next week is: ", dte)
    #scan_options( client, stocks, quotes, dte)
    
    
    # pprint.pprint( quotes )
    # pprint.pprint( quotes['TSLA'] )

    # Saves information about my account
    # account_req = ["positions", "orders"]
    # accounts = client.get_accounts( account="all", fields=account_req )
    # pprint.pprint( accounts )

    # Steps:
    #   1. Look at options at certain strike price
    #   2. Evaluate the value / cost. If corret return. 

    return



if __name__=="__main__":
    main()


