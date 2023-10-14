# TODO: make header

from os import listdir
from os.path import isfile, join
import re
import shutil


def makeOneGlobalCsv():

    # Makes a list of all converted files
    # TODO: Don't hard code this
    transaction_path = "/Users/phoot/code/finance/sensitive_files/"
    global_transactions_file = transaction_path + "/global_transactions.csv"
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
    file = Path( global_transactions_file )
    if file.is_file():
        os.rename( global_transactions_file, global_transactions_file_backup )

    file = Path( global_transactions_file_backup )
    if file.is_file():
        os.remove( global_transactions_file_bakcup )

    # Appends all the found converted files to the global csv
    count = 0
    for file in converted_files:
        base_file = ""
        if count == 0:
            shutil.copyfile( transaction_path + str( file ), global_transaction_path )
            with open( transaction_path + file, 'r' ) as base:
                base_file = base.read()
                print( str( base_file ) )
            count += 1

        else:
            with open( transaction_path + file, 'r' ) as file_open:
                file_open.write( str( base_file ) )

   # with open('original.csv', 'r') as f1:
   #     original = f1.read()
   # 
   # with open('all.csv', 'a') as f2:
   #     f2.write('\n')
   #     f2.write(original)

    
    global_csv_name = "Fixme"
    return global_csv_name

def main():
    name = makeOneGlobalCsv()

    print( __name__ + ": " + name )

    return
# functions # Filter out stocks


if __name__ == "__main__":
    main()
