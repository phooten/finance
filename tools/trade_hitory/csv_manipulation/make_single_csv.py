# TODO: make header

import os
from messages import class_messages
from os import listdir
from os.path import isfile, join
import re
import shutil

msg = class_messages.messages()

def makeOneGlobalCsv():

    # Makes a list of all converted files
    # TODO: Don't hard code this
    transaction_path = "/Users/phoot/code/finance/sensitive_files/"
    global_transactions_file = transaction_path + "global_transactions.csv"
    global_transactions_file_backup = global_transactions_file + "_BACKUP.csv"
    all_sensitive_files = [ file for file in listdir(  transaction_path )if isfile( join( transaction_path, file ) ) ]
    #print( __name__ + ": all files: " + str( onlyfiles ) )

    converted_files = []
    pattern = re.compile( "^converted_transactions_20[0-9][0-9]\.csv$" )
    for file in all_sensitive_files:
        if pattern.match( str( file ) ):
            converted_files.append( file )
            msg.system( "Found file to append '" + file + "'", __name__ )

    # Makes a backup of the global file if it exists, and removes the back up if it exists
    if os.path.exists( global_transactions_file_backup ):
        msg.system( "Old backup file removed under the name '" + global_transactions_file_backup + "'", __name__ )
        os.remove( global_transactions_file_backup )

    if os.path.exists( global_transactions_file ):
        msg.system( "Old file renamed to '" + global_transactions_file + "'", __name__ )
        os.rename( global_transactions_file, global_transactions_file_backup )

    # Appends all the found converted files to the global csv
    count = 0
    base_file = ""
    gf = open( global_transactions_file , "w" )
    for file in converted_files:
        with open( transaction_path + str( file ), "r" ) as tf:
            msg.system( "looking through file '" + file + "'", __name__ )
            gf.write( tf.read() )
            tf.close()

    gf.close()


    msg.system( "New file created under the name '" + global_transactions_file + "'", __name__ )

    return global_transactions_file


def convertAllAvailableCsvFiles():
    """
    Description:    
    Arguments:      
    Returns:        
    """

    mypath = "/Users/phoot/code/finance/sensitive_files"
    onlyfiles = [ f for f in listdir( mypath ) if isfile( join( mypath, f ) ) ]

    # TODO This needs to not be hard coded
    regex_pattern_transactions = "^transactions_20[0-9][0-9]\.csv$"
    regex_pattern_transactions_converted = "^converted_transactions_20[0-9][0-9]\.csv$"

    pattern_transactions = re.compile( regex_pattern_transactions )
    pattern_transactions_converted = re.compile( regex_pattern_transactions_converted )

    # TODO: warn if already converted
    # TODO: Don't hard code single file conversion
    for file in onlyfiles:
        if pattern_transactions.match( file ):
            print( "found a file to convert '" + file + "'" )


    #    msg.error( "\nIncorrect file format: '" + args.input_file + "'\n"\
    #               "See regex pattern:     '" + regex_pattern + "'\n",
    #                __name__ )
    #    return False, args.input_file
    #file = ""

    # Find all the transaction files

    # If converted file already, note that to operator

    # If not, convert file and notify operator

    return


def refineFile( raw_file ):
    """
    Description:    Removes headers that appear more than once and re-numbers the first column into a total order
    Arguments:      Raw file of the global file that was appended together
    Returns:        Void
    """

    #with 

    return

def main():
    convertAllAvailableCsvFiles()

    file = makeOneGlobalCsv()

    refineFile( file )

    return


if __name__ == "__main__":
    main()

