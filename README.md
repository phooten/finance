# How to run:
    * Pre-requisits:
        - Set up a developer account with TDA Ameritrade API
        - 
    * Setup
        pipenv install
        pipenv shell
        pipenv run <python3> <python-file.py>
        ( if in vscode, run with debugger )
        exit

# Repository Contents
input:  files containing list of stocks used for various tools
output: files containing output from tools that were run.
tools:  useful for various tasks relating to trading
util:   utility files for this repo


# REPO 'finance' TODOS:
1. Finish the informative tools script about my current account
2. Create a "showme" or something for how to show tools and usage.


# Tool Improvement Ideas
1. Show cost basis / profit vs loss for each stock. Maybe this can be used to show
    the status of my account. 
2. Scanner to show if if a stock drops more than 30-40% in a day.



# Notes
Really good video for how to get started: https://www.youtube.com/watch?v=8N1IxYXs4e8
    inside the .env file
        - Consumer Key
            -> also known as: Client ID, Token
            -> can be found
        - Redirect URI
            -> found on the 'tda developer api'
            -> Also known as Callback URI
        - JSON Path
            ->


# Current issue
Messed up and removed files that were being tracked by git ignore:
    .env
    token.json
Need to make a template for these so this doens't happen again, or it will at 
least be easier to recover.


# References:
    - tutorial: https://www.youtube.com/watch?v=8N1IxYXs4e8
    - tda developer api: https://developer.tdameritrade.com/user/me/apps
