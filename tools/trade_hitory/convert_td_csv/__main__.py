#!/bin/

# Overview:
#   Every year, download a TD Ameritrade history of my trades. At any point,
#   download the current year to add to the list. 
#


# Modules
import csv
import os
import pandas as pd
import sys
import inspect

# Project Modules
parent_dir = os.path.dirname( os.path.realpath( __file__ ) )    # Get the parent directory
sys.path.append( parent_dir )                                 # Add the parent directory to sys.path
from messages import class_messages
from utility import helper_functions
#from utility import class_filter_csv

msg = class_messages.messages()

def main():

    # TODO: Change this for an argument
    #       For now, dev hard codes which file to use
    dev_selected = 1
    csv_input_names = [ 'test_transactions_2022.csv',
                        'transactions_2021.csv',
                        'transactions_2022.csv' ]
    csv_input_name = csv_input_names[ dev_selected ]

    # Intial checks for the csv file
    sensitive_path = '../../../sensitive_files/'
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


if __name__ == "__main__":
    main()
