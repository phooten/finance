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
def scan_options( client, stocks, quotes ):
    # TODO: print out stock only if there is a match
    for curr_stock in stocks:
        print( "---------------------------------------------------")
        print( "Stock:\t\t" + str(curr_stock))

        dte = ( datetime.today() + timedelta(days=10) ).date()
        print("Next week is: ", dte)

        stock_info_j = client.get_quote(curr_stock).json()[curr_stock]
        stock_price = stock_info_j['mark']
        strike_start = int( stock_price )
        strike_interval = 1
        strike_range = 10

        # volatility = 

        # Ideas:
        #   1. Only show option if correct otm% and value. have a total count
        #   2. Flag to print out the options if I want to, or only those from 1.
        print("Current price:\t" + str(stock_price))

        # Settings:
        # delta_max = 0.9
        group = 1
        if group == 1:
            a = 1
            b = 80
        elif group == 2:
            a = 1
            b = 85
        elif group == 3:
            a = 1.5
            b = 80

        value_min = a / 100
        otm_prob_min = ( b / 100 ) - 0.02
        otm_prob_max = 100 / 100
        bid_min = 0.10  # minimum bid size ( $ 10 )
        bid_diff_max = 0.30  # Biggest difference in asking size

        op_chain = client.get_option_chain( symbol=curr_stock,
                                            to_date=dte,
                                            # strike=strike_curr,
                                            contract_type=client.Options.ContractType.PUT)
        op_chain_j = op_chain.json()
        op_chain_expmap = op_chain_j['putExpDateMap']
        # Checks the chain exists
        if not bool(op_chain_expmap):
            print("No results for strike: " + str(curr_stock))
            continue

        # Checks each strike in the date
        for date in op_chain_expmap:
            for strike in op_chain_expmap[date]:

                # Gathers variables to filter
                strike_map = op_chain_expmap[date][strike][0]
                mark = float(strike_map['mark'])
                value = mark / float(strike)
                delta = strike_map['delta']
                otm_prob = 1 + float(delta)
                # print(json.dumps(strike_map, indent=4))
    
                # break
                # bid/ask needs to be reasonably close together, or bid needs to be > 1
                bid_curr = strike_map['bid']
                ask_curr = strike_map['ask']
                bid_diff = abs( int(ask_curr) - int(bid_curr) )

                # Filters out what is wanted
                if ( value > value_min ) and ( otm_prob > otm_prob_min ):
                    # if bid_diff > bid_diff_max:
                        # print("\n** Large difference in bid / ask.\nbid: " + str(bid_curr) + "\nask:" + str(ask_curr) + "\n")

                    # if bid_curr > bid_min:
                    print( "[ " + str(date) + " ]\t" +\
                        "Stike: " + str(strike) +
                        "\tMark: " + str(mark) +\
                        "\tBid: " + str(bid_curr) +\
                        "\tValue: {0:.2%}".format(value) + "  [{0:.3}]".format(value) +\
                        "\tDelta: " + " {0:.3}".format(delta) + " [ {0:.2%} ]".format(otm_prob))

    return



# Driver of the code
def main():
    # TODO: Add a func / feature to have user input for path, and if not use default. 
    # Set Up
    client = CreateClient()

    stocks = GetInputStocks()
    quotes = client.get_quotes(stocks)
    #print(json.dumps(quotes.json(), indent=4 ))
    

    scan_options( client, stocks, quotes )
    
    
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


