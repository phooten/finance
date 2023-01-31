# Overview:
#   This tool is meant to scan a list of stocks and return certain values. The 
#   requirements for this file can be found in the same file path, but labeled
#   requirements.



import os
import math
from tda import auth, client
import httpx
import datetime as dt
from dotenv import load_dotenv
import chromedriver_autoinstaller

# Trade Settings
symbol = os.getenv('SYMBOL')
target_dte = int(os.getenv('TARGET_DTE'))
trade_type = (os.getenv('TRADE_TYPE'))
otm_price_target = float(os.getenv('OTM_PRICE_TARGET'))
otm_percent_target = float(os.getenv('MIN_OTM_PERCENT'))
spread_price_target = float(os.getenv('SPREAD_PRICE_TARGET'))
spread_width_target = float(os.getenv('SPREAD_WIDTH_TARGET'))


# Retrieves a list of stocks from a text file and returns it as a list
def GetInput():
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



# TDA Function
def GetQuote(symbol, c):
    q = c.get_quote(symbol)
    assert q.status_code == httpx.codes.OK, q.raise_for_status()
    return q.json()



def GetOptionChain(c: client.Client):
    r = c.get_option_chain(symbol=symbol, strike_range=client.Client.Options.StrikeRange.OUT_OF_THE_MONEY, option_type=client.Client.Options.Type.STANDARD, from_date=dt.datetime.now() + dt.timedelta(days=target_dte-10), to_date=dt.datetime.now() + dt.timedelta(days=target_dte+10)  )
    assert r.status_code == httpx.codes.OK, r.raise_for_status()
    return r.json()



def CreateClient():
    token_path = 'token.json'
    api_key = f"{os.getenv('API_KEY')}@AMER.OAUTHAP"
    redirect_uri = os.getenv('REDIRECT_URI')

    try:
        c = auth.client_from_token_file(token_path, api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome() as driver:
            c = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)
                
    return c



def GetOtmStrike(closest_exp: dict, ticker: dict):
    distance = math.inf
    otm_strike = None
    for details in closest_exp.values():
        short = next((type for type in details if type['settlementType'] == 'P'), None)

        if short is None:
            continue

        percent_otm = abs(1 - (short['strikePrice'] / ticker[symbol]['lastPrice']))
        if otm_percent_target > 0 and percent_otm < otm_percent_target:
            continue
            
        price = (short['bid']+short['ask'])/2
        delta = abs(otm_price_target - price)
        if delta < distance:
            distance = delta
            otm_strike = short
    return otm_strike



def GetSpreadStrikes(spread_price_target: float, spread_width_target: float, closest_exp: dict):
    distance = math.inf
    best_short = None
    best_long = None
    price_width = 0.0
    for short_strike, short_details in closest_exp.items():
        short_strike = float(short_strike)
        long_strike = str(short_strike + spread_width_target)

        long_details = closest_exp.get(long_strike)

        if long_details is None:
            continue

        short = next((type for type in short_details if type['settlementType'] == 'P'), None)
        long = next((type for type in long_details if type['settlementType'] == 'P'), None)

        if short is None or long is None:
            continue
        
        price_width = (long['ask']+long['bid'])/2 - (short['ask']+short['bid'])/2

        delta = abs(spread_price_target - price_width)

        if delta < distance:
            distance = delta
            best_price = price_width
            best_short = short
            best_long = long
    return best_short,best_long,best_price



# Driver of the code
def main():
    stocks = GetInput()
    print( stocks )

    # Have the list of stocks, now run a scan over them. 
    # Setup Client
    c = create_client()

    # Get the Option Chain
    option_chain = GetOptionChain( c )

    if trade_type in ["1.1.2", "1.1.1"]:
        spread_expiry = GetExpiration( option_chain[ 'putExpDateMap' ] )
        otm_expiry = spread_expiry

    elif trade_type == "Bear 1.1.2":
        # Get Closest Expiration
        spread_expiry = GetExpiration( option_chain[ 'putExpDateMap' ] )
        otm_expiry = GetExpiration( option_chain[ 'callExpDateMap' ] )

    # Get Current Price
    ticker = GetQuote( symbol, c )

    # Find OTM Strike
    otm_put = GetOtmStrike( otm_expiry, ticker )

    # Find Spread
    best_short, best_long, best_price = GetSpreadStrikes( spread_price_target, spread_width_target, spread_expiry )

    if trade_type == "1.1.1":
        otm_count = 1
    elif trade_type in [ "1.1.2", "Bear 1.1.2" ]:
        otm_count = 2
    else:
        otm_count = 0
    
    # Print Results
    print( f"{otm_count}x {otm_put['description']}" )
    print( f"1x {best_short['description']}" )
    print( f"1x {best_long['description']}" )
    print( f"Short Premium: {otm_count}x ${(otm_put['bid'] + otm_put['ask'])/2}" )
    print( f"Spread Premium: 1x ${best_price}" )
    print( f"Total Premium: ${otm_count*float((otm_put['bid'] + otm_put['ask'])/2) - float(best_price)}" )
    print( f"Protection: {100*(1-(otm_put['strikePrice']/ticker[symbol]['lastPrice']))}%" )
    return



if __name__=="__main__":
    main()


