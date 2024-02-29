# TODO: Complete / remove all TODOs. 
# TODO: Create requirements for this tool

"""
*********************************** DISCLAIMER: ********************************
I ( or this code ) am not responsable for any financial losses or gains incured from the use of this program / software. 
This is purally for personal use and educational purposes. Feel free to look through this code or use for fun.

Don't use this for any real life financial analysis or information. There are most likley many errors in here. 

Proceed at your own risk. 
********************************************************************************


Overivew: 
    Scans options / puts based on user input for strikes that meet certain criteria.

    Program scans for list of stocks contained under <workspace path>/input. See that location's README for more info.
    This scan is based on a hardcoded settings. There is no intension of allowing the user to change these, since they
    are tuned based on trial and error, and set for a low risk tolerance while allowing for maximum value reward. You
    can manually change these, but proceed with caution. Review the disclaimer above. 

Strikes only analyzed if: 
    - within X days from today: 10
    - within X ticks OTM:       10
    - Bid minimum is:           0.10
    - Bid / Ask diff is:        0.30
    - Probability OTM:          82.0 % ( put )
                                85.0 % ( call )
    - Value:                    1.00 % ( put ) ( potential gain / capital used )
                                0.25 % ( call )
Note: Settings are according to infor returned from TD Ameritrade API. 
Note: Probabilities are based on DELTA.


Typical usage example:
    python value_scan.py -e
    python value_scan.py -c -s <some-list-here>.txt
    python value_scan.py -p -s <some-list-here>.txt


References:
    API: https://tda-api.readthedocs.io/en/latest/client.html#option-chain
         alternative API library: 'from td.client import TDClient'
    Based on: https://github.com/pattertj/TDA-Trade-Scripts/blob/main/main.py
"""

# Imports 
import argparse
import chromedriver_autoinstaller
import datetime as dt
import httpx
import json
import math
import os
import pprint
import subprocess
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from tda import auth, client

# Global Variables
load_dotenv()

# Retrieves a list of stocks from a text file and returns it as a list
def GetInputStocks( stock_input_list ):

    # TODO: Hard coding needs to be replaced with environment variables
    # Paths / locations 
    #REPO_PATH = "/Users/phoot/code/finance"
    REPO_PATH = os.environ['REPO_PATH']
    THIS_PATH = str(REPO_PATH) + "/tools/options_scanner"
    THIS_NAME = os.path.basename(__file__)
    # INPUT_NAME="list-1.txt"
    INPUT_NAME=stock_input_list
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
    # TODO: Add feature to ignore any lines prefaced with '#' or just blank
    stock_list = file.readlines()
    file.close()

    stocks = []
    for entry in stock_list:
        # TODO: function to check stocks for validity
        stocks.append( entry.replace("\n", "") )

    return stocks


# TODO: Fix header comment
# Builds and returns the client based on token and envirenmental variables. 
def CreateClient():
    try:
        print("Try: TOKEN_PATH = '" + str(os.getenv("TOKEN_PATH")) + "'")
        print("Try: REPO_PATH = '" + str(os.getenv("REPO_PATH")) + "'")
        c = auth.client_from_token_file( str(os.getenv("TOKEN_PATH")), 
                                         str(os.getenv("CONSUMER_KEY")))

    except:
        from selenium import webdriver
        with webdriver.Chrome() as driver:
            print("Except: TOKEN_PATH = '" + str(os.getenv("TOKEN_PATH")) + "'")
            print("Except: REPO_PATH = '" + str(os.getenv("REPO_PATH")) + "'")
            c = auth.client_from_login_flow( driver, 
                                             api_key=str(os.getenv("CONSUMER_KEY")),
                                             redirect_url=str(os.getenv("REDIRECT_URI")),
                                             token_path=str(os.getenv("TOKEN_PATH")) )

    return c

# TODO: Fix this header
# Scans a list of options ( puts or calls ) based on input text file list from user
# and prints out applicable strikes based on options. Current settings:
# 
# Puts:
#   1. > 80% OTM
#   2. Difference between bid / ask < 0.10
#   3. Value ( money used vs. profit gained ) > 1%
# 
# Calls:
#   1. > 80% OTM
#   2. Difference between bid / ask < 0.10
#   3.
def ScanOptions( client, stocks, quotes, option ):
    # TODO: print out stock only if there is a match
    # TODO: Create a spot for ALL settings. Maybe as globals?

    print_to_file = False
    if print_to_file == True:
        result_obj = open("/Users/phoot/code/finance/option_scan_results.txt", "w")

    for curr_stock in stocks:
        dte = ( datetime.today() + timedelta(days=10) ).date()

        stock_info_json = client.get_quote(curr_stock).json()[curr_stock]
        # print( json.dumps(stock_info_json, indent=4))
        # break
        stock_price = float( stock_info_json['mark'] )
        close_price = float(stock_info_json['closePrice'])
        net_change = float(stock_info_json['netChange'])
        percent_change = net_change / close_price
        strike_start = int(stock_price)
        strike_interval = 1
        strike_range = 10

        # volatility = 

        # Ideas:
        #   1. Only show option if correct otm% and value. have a total count
        #   2. Flag to print out the options if I want to, or only those from 1.
        if print_to_file == True:
            result_obj.write("---------------------------------------------------")
            result_obj.write("Stock:\t\t" + str(curr_stock))
            result_obj.write("Next week:\t" + str(dte))
            result_obj.write("Current price:\t$ {0:.2f}".format(stock_price))
            result_obj.write("Net Change:\t% {0:.2%}".format(percent_change))
        else:
            print( "---------------------------------------------------")
            print( "Stock:\t\t" + str(curr_stock))
            print("Next week:\t" + str(dte))
            print("Current price:\t$ {0:.2f}".format(stock_price))
            print("Net Change:\t% {0:.2%}".format(percent_change))


        # Settings:
        if option == "put":
            contract_type = client.Options.ContractType.PUT
            option_map = 'putExpDateMap'
            val_num = 1    # % value ( numerator ) -> Default = 1 %
            # val_num = 0.85    # % value ( numerator ) -> This is better to change than probability
            prob_num = 80   # % OTM ( numerator ) -> Default = 85 %

        elif option == "call":
            contract_type = client.Options.ContractType.CALL
            option_map = 'callExpDateMap'
            # w/ 85% OTM, These values are not that common: 0.25%, 
            val_num = 0.05  # % value ( numerator )
            # val_num = 0.20  # % value ( numerator )
            prob_num = 85   # % OTM ( numerator )

        else:
            print( "Should neve get here. Error. Exiting." )
            exit(1)

        value_min = val_num / 100
        otm_prob_min = ( prob_num / 100 ) - 0.02
        otm_prob_max = 100 / 100
        bid_min = 0.10  # minimum bid size ( $ 10 )
        bid_diff_max = 0.30  # Biggest difference in asking size


        op_chain = client.get_option_chain( symbol=curr_stock,
                                            to_date=dte,
                                            # strike=strike_curr,
                                            contract_type=contract_type )

        op_chain_j = op_chain.json()
        op_chain_expmap = op_chain_j[option_map]

        # Checks the chain exists
        if not bool(op_chain_expmap):
            if print_to_file == True:
                result_obj.write("No results for strike: " + str(curr_stock))
            else:
                print("No results for strike: " + str(curr_stock))
            continue

        # Checks each strike in the date
        for date in op_chain_expmap:
            for strike in op_chain_expmap[date]:
            # print(json.dumps(op_chain_j, indent=4))
            # break

                # Gathers variables to filter
                strike_map = op_chain_expmap[date][strike][0]
                mark = float(strike_map['mark'])
                value = mark / float(strike)
                delta = strike_map['delta']
                if option == "call":
                    delta = float(delta) * (-1)
                otm_prob = 1 + float(delta)

                # bid/ask needs to be reasonably close together, or bid needs to be > 1
                bid_curr = strike_map['bid']
                ask_curr = strike_map['ask']
                bid_diff = abs( int(ask_curr) - int(bid_curr) )

                # Filters out what is wanted
                if ( value > value_min ) and ( otm_prob > otm_prob_min ) and ( bid_curr > 0.10):

                    if print_to_file == True:
                        # if bid_diff > bid_diff_max:
                            # print("\n** Large difference in bid / ask.\nbid: " + str(bid_curr) + "\nask:" + str(ask_curr) + "\n")
                        result_obj.write("[ " + str(date) + " ]\t" +
                            "Stike: " + str(strike) +
                            "\tMark: " + str(mark) +
                            "\tBid: " + str(bid_curr) +
                            "\tValue: {0:.2%}".format(value) + "  [ {0:.3} ]".format(value) +
                            "\tDelta: " + " {0:.3}".format(delta) + " [ {0:.2%} ]".format(otm_prob))
                    else:
                        # if bid_curr > bid_min:
                        print( "[ " + str(date) + " ]\t" +\
                            "Stike: " + str(strike) +
                            "\tMark: " + str(mark) +\
                            "\tBid: " + str(bid_curr) +\
                            "\tValue: {0:.2%}".format(value) + "  [ {0:.3} ]".format(value) +\
                            "\tDelta: " + " {0:.3}".format(delta) + " [ {0:.2%} ]".format(otm_prob))



    return

# TODO: Fix this header
# Pasrses the document and only prints the found stocks
def PrintFound():

    return

# TODO: Fix this header
# Driver of the code
def main():
    # TODO: Add a func / feature to have user input for path, and if not use default. 
    parser = argparse.ArgumentParser()
    parser.add_argument( "-s", "--stock_list", 
                        default="puts_mid-priced.txt",
                        required=False,
                        help="List of stocks used to query for puts. Held under <home-path>/code/finance/input/" )
    parser.add_argument( "-o", "--option_type",
                         default="put",
                         required=False,
                         help="List of stocks used to query for calls. Options are 'put' or 'call'")
    parser.add_argument("-e", "--example_cases",
                        # default=False,
                        action='store_true',
                        required=False,
                        help="Shows current tool usage cases.")
    args = parser.parse_args()

    if args.example_cases:
        example_cases = "\n"\
            "python /Users/phoot/code/finance/tools/options_scanner/value_scan.py -o <put|call> -s <see_list_below>\n"
        print( example_cases )
        subprocess.call(
            ['sh', '/Users/phoot/code/finance/tools/utility/show_stock_lists.sh'])
        exit(1)

    stock_input_list = args.stock_list
    option = args.option_type
    
    # Set Up
    client = CreateClient()

    stocks = GetInputStocks( stock_input_list )
    quotes = client.get_quotes( stocks )
    #print(json.dumps(quotes.json(), indent=4 ))
    
    ScanOptions( client, stocks, quotes, option )

    
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


# TODO: Fix this header

if __name__=="__main__":
    main()
    # TODO: Make a status bar for querying stocks
    # TODO: Update the options flag to a true / false so the user doesn't have to specify 'call'/'put'. They can just
    #       run '-c' or '-p'. 


