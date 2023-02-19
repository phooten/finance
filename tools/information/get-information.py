# Overview:
#   This tool is meant to scan a list of stocks and return certain values. The 
#   requirements for this file can be found in the same file path, but labeled
#   requirements.

# TODO: initial revision was copied from here: https://github.com/pattertj/TDA-Trade-Scripts/blob/main/main.py
#       Need to refine calls and make it unique to my use case. 

import pprint
import os
import math
# from tda import auth, client
import httpx
import datetime as dt
from dotenv import load_dotenv
import chromedriver_autoinstaller

from td.client import TDClient

# Global Variables
G_TOKEN=os.getenv('TOKEN_PATH')


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

    account_req = ["positions", "orders"]
    set_a = [""]
    accounts = client.get_accounts( account="all", fields=account_req)
    pprint.pprint( accounts )
    return



if __name__=="__main__":
    main()


