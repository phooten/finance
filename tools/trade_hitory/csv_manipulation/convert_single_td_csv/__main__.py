#!/bin/

# Overview:
#   Every year, download a TD Ameritrade history of my trades. At any point,
#   download the current year to add to the list. 
#


# Modules
import argparse
import csv
import os
# import pandas as pd
import re
import sys
import inspect

# Project Modules
parent_dir = os.path.dirname( os.path.realpath( __file__ ) )    # Get the parent directory
sys.path.append( parent_dir )                                 # Add the parent directory to sys.path
from HootLogger import logger
from utility import helper_functions
#from utility import class_filter_csv

msg = logger.messages( __name__ )
#msg = class_messages.messages()

def main():
    
    # TODO: Change this for an argument
    #       For now, dev hard codes which file to use
    dev_selected = 3
    csv_input_names = [ 'transactions_2021.csv',
                        'transactions_2022.csv',
                        'transactions_2023.csv',
                        'transactions_2024.csv' ]
    csv_input_name = csv_input_names[ dev_selected ]

    # Gets file to convert
    sensitive_path = '/Users/phoot/code/finance/sensitive_files/'
    passed, csv_input_name = getInputFile()
    if passed == False:
        msg.quit_script()

    # Intial checks for the csv file
    csv_input_path =  sensitive_path + csv_input_name
    passed = helper_functions.initialCsvFileCheck( csv_input_path )
    if not passed:
        msg.quit_script()

    # Checks basic content of the csv files
    passed = helper_functions.contentsCsvFileCheck( csv_input_path )
    if not passed:
        msg.quit_script()

    # Transfers input csv data into an output csv
    csv_output_path =  sensitive_path + "converted_" + csv_input_name
    passed = helper_functions.transferCsvContents( csv_input_path, csv_output_path )
    if not passed:
        msg.quit_script()

    msg.quit_script()

    # Handle the output file
    # try:
    #     os.remove( csv_output_path )
    # except:
    #     print( "No files in this path: ", csv_output_path )
    # df.to_csv( csv_output_path )
    
    # new_csv.set_index( 'INDEX' )
    try:
        os.remove( csv_output_path )
    except:
        print( "No files in this path: ", csv_output_path )
    new_csv.to_csv( csv_output_path, index=False )

    return


def getInputFile():
    """
    Description:    
    Arguments:      
    Returns:        
    """
    parser = argparse.ArgumentParser( description='Process some integers.' )
    parser.add_argument( '-f',
                         '--file',
                         metavar='File',
                         dest='input_file',
                         required=True )

    args = parser.parse_args()

    # TODO: Don't hard code this. use environmental variables
    regex_pattern = "^transactions_20[0-9][0-9]\.csv$"
    pattern = re.compile( regex_pattern )
    if not pattern.match( args.input_file ):
        msg.error( "\nIncorrect file format: '" + args.input_file + "'\n"\
                   "See regex pattern:     '" + regex_pattern + "'\n",
                    __name__ )
        return False, args.input_file

    return True, args.input_file



if __name__ == "__main__":
    main()
