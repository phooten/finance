# About
This repository is meant to track different financial programs and scripts. As long as the tools are relativley
small, they are all tracked in here. Sensitive files have been exlcluded, but there are some test files that can be
seen to use for practice or comparison.

## Tools: Complete
None.

## Tools: In-progress
trade_history tool set:
    convert_single_td_csv:
        After downloading a csv of trade history from a platform ( currently only working with TD Ameritrade ), the script
        converts the details into a more consistant / readable csv format

    make_single_csv.py:
        Finds all the csv's that have been converted by "convert_single_td_csv", then condenses them into a single csv
        file.

    filter details:
        Uses the results from make_single_csv.py to gather and filter information into a readable format.

convert_paycheck:   Takes a paycheck pdf and converts it into an easily read format to append to an excel file.

                    STATUS: Non-working state.


scan_option_value:  scans a selected list of stocks that will return a list based on a given set of risk vs. rewards
                        settings.
                        Status: working state, but rudimentary.

## Tools: Future Ideas
stock_overview: QT Centered UI that allows user to sort through an excel file for statistics like how much money has
                been gained or lost on a single company, how many options were sold / lost, average amount gained
                from options in a week, etc.

show_tools:     script to list all all tools and the progress / state of them at a quick glance


scan_large_change:  Scanner to show if if a stock drops more than 30-40% in a day.




# Setup for use
1. Pre-requisits:
    If using a script related to TD Ameritrade:
        * Set up a developer account with TDA Ameritrade API
2. Setup
    pipenv install
    pipenv shell
    pipenv run <python3> <python-file.py>
    ( if in vscode, run with debugger )
    exit
    ( when ready to be done / exit pipenv )



# This repository TODOs
* Research ways to:
    1. Structure projects i.e. output / input, tools, bin, etc.
    2. Work with envirnmental variables across the project
* Fill out "contents / navigation" section in the readme




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




# References / Resources
    - tutorial: https://www.youtube.com/watch?v=8N1IxYXs4e8
    - tda developer api: https://developer.tdameritrade.com/user/me/apps
