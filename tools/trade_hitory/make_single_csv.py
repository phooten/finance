# TODO: make header

import os
from os import listdir
from os.path import isfile, join
import re
import shutil


def makeOneGlobalCsv():

    # Makes a list of all converted files
    # TODO: Don't hard code this
    transaction_path = "/Users/phoot/code/finance/sensitive_files/"
    global_transactions_file = transaction_path + "global_transactions.csv"
    global_transactions_file_backup = global_transactions_file + ".bak"
    all_sensitive_files = [ file for file in listdir(  transaction_path )if isfile( join( transaction_path, file ) ) ]
    #print( __name__ + ": all files: " + str( onlyfiles ) )

    converted_files = []
    pattern = re.compile( "^converted_transactions_20[0-9][0-9]\.csv$" )
    for file in all_sensitive_files:
        #print( __name__ + ": file => " + file )
        if pattern.match( str( file ) ):
            converted_files.append( file )
            #print( __name__ + ": Found file: " + file )

    # Makes a backup of the global file if it exists, and removes the back up if it exists
    if os.path.exists( global_transactions_file_backup ):
        print( __name__ + ": Old backup file removed under the name '" + global_transactions_file_backup + "'" )
        os.remove( global_transactions_file_backup )

    if os.path.exists( global_transactions_file ):
        print( __name__ + ": Old file renamed to '" + global_transactions_file + "'" )
        os.rename( global_transactions_file, global_transactions_file_backup )

    # Appends all the found converted files to the global csv
    count = 0
    base_file = ""
    gf = open( global_transactions_file , "w" )
    for file in converted_files:
        with open( transaction_path + str( file ), "r" ) as tf:
            print( __name__ + ": looking through file '" + file + "'" )
            gf.write( tf.read() )
            tf.close()
   # for file in converted_files:
   #     if count == 0:
   #         shutil.copyfile( transaction_path + str( file ), global_transactions_file )
   #         count += 1

   #     else:
   #         with open( global_transactions_file, 'a' ) as global_file:
   #             with open( transaction_path + file, 'r' ) as file_open:
   #                 global_file.write( file_open  )
   #                 file_open.close()

    gf.close()


    print( __name__ + ": New file created under the name '" + global_transactions_file + "'" )

    return

def main():
    makeOneGlobalCsv()

    #print( __name__ + ": " + name )
    return


if __name__ == "__main__":
    main()

