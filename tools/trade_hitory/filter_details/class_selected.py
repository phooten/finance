import pandas as pd


class UserSelection:
    def __init__( self ):
        # String of selected Tickers
        mSelectedTickers = []
        mAvailableTickers = [ "TSLA", "AAPL", "F", "MSFT" ]

        # String of selected Types
        mSelectedType = []
        mAvailableType = [ "Other", "Options", "Stocks" ]

        # Selected Dates
        mStartDate = ""
        mEndDate = ""

        # Dataframes for the object
        # TODO: Need to initialize the dataframe
        _mOriginalDataframe = pd.read_csv( "/Users/phoot/code/finance/sensitive_files/global_transactions.csv" )
        #_mCurrentDataframe

    #def setSelectedTickers();
    #    return

    #def setSelectedTypes():
    #    return

    #def setSelectedStartDate():
    #    return

    #def setSelectedEndDate():
    #    return

    def setOriginalDataframe( self, dataframe ):
        _mOriginalDataframe = dataframe
        return True

    #def setCurrentDataframe():
    #    return

    #def getSelectedTickers():
    #    return

    #def getSelectedTypes():
    #    return

    #def getSelectedStartDate():
    #    return

    #def getSelectedEndDate():
    #    return

    def getOriginalDataframe( self ):
        return _mOriginalDataframe

    #def getCurrentDataframe():
    #    return
