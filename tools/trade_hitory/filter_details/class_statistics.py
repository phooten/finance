
import os
import pandas as pd
from messages import class_messages
import class_selected

# TODO: Go back and and add in checks / unit tests


class statistics:
    def __init__( self ):

        self.mUserSelection = class_selected.UserSelection()
        msg = class_messages.messages()

        self.run()

        return

    def run( self ):
        self.readInputCsv()
        return


    def readInputCsv( self ):
        # TODO: Don't hard code this
        global_path = "/Users/phoot/code/finance/sensitive_files/global_transactions.csv"

        self.mUserSelection.setOriginalDataframe( pd.read_csv( global_path ) )
        row_count, column_count = df.shape
        df_header = df.columns.value

        msg.system( "Dataframe Found:\n" + str( mUserSelection.getOriginalDataframe() ), __name__ )

        return


