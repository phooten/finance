
# Modules
import sys

# Project Modules
#   NA


class messages:

    def error( self, msg, func_name ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """

        print( "\n" )
        print( "--------------------" )
        print( "ERROR:" )
        print( func_name + ": " + msg )
        print( "--------------------" )

        return

    def system( self, msg, func_name ):
        """
        Description:    Prints out message to the user
        Arguments:      msg     - (string) to be printed out to user
                        func_name - (function) function called that figures out what the 
                                name of the previous funcion is
        Returns:        Void
        """

        print( "\n" )
        print( func_name + ": " + msg )

        return

    def quit_script( self ):
        print( "Exiting script.")
        exit(1)

