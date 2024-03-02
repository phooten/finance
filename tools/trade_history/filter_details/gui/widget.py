# This Python file uses the following encoding: utf-8
import sys
import subprocess

from PySide6 import QtCore                          # Needed for DateTypes
from PySide6.QtWidgets import QApplication, QWidget

import sys                                          # Needed to get virtualenv interpreter

# Important:
# You need to run the following command to generate the ui_form.py file for ANY updates
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

class Widget( QWidget ):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Connecting buttons to clicked functions
        self.ui.filterButton.clicked.connect( self.filterButtonPressed )
        self.ui.exitButton.clicked.connect( self.exitButtonPressed )

        return

    def filterButtonPressed( self ):
        # Gets the dates ranges. Current year by default
        start_date = self.ui.dateEditStart.date().toString( QtCore.Qt.ISODate )
        end_date = self.ui.dateEditEnd.date().toString( QtCore.Qt.ISODate )
        print( "Start Date: " + str( start_date ) )
        print( "End Date:   " + str( end_date ) )

        # Offset
        offset = "0.00"

        # Stock List
        ticker_list = "\"TSLA AAPL\""

        # Type
        if self.ui.radioButtonAll.isChecked():
            sort_type = self.ui.radioButtonAll.text().lower()

        elif self.ui.radioButtonOptions.isChecked():
            sort_type = self.ui.radioButtonOptions.text().lower()

        elif self.ui.radioButtonPuts.isChecked():
            sort_type = self.ui.radioButtonPuts.text().lower()

        elif self.ui.radioButtonCalls.isChecked():
            sort_type = self.ui.radioButtonCalls.text().lower()

        elif self.ui.radioButtonStocks.isChecked():
            sort_type = self.ui.radioButtonStocks.text().lower()

        else:
            print( "Error: no radio button selected" )
            sort_type = ""

        # TODO: Hardcoded for now
#        script_path = "/Users/phoot/code/finance/tools/trade_history/filter_details/test.py"
        script_path = "/Users/phoot/code/finance/tools/trade_history/filter_details/find_total_profit.py"

        # By default, python runs /usr/bin/python in scripts. If we're using a virtual environment
        # modules might not be installed so we have to specify the exact interpreter we're using
        interpreter = str( sys.executable )

        # Builds the command and runs the filter script
        command_list = [ interpreter, script_path, \
                            "--start_date", start_date, \
                            "--end_date", end_date, \
                            "--ticker_list", ticker_list, \
                            "--sort_type", sort_type, \
                            "--offset", offset ]
        command = " ".join( command_list )

        subprocess.call( command, shell=True )
        return


    def exitButtonPressed( self ):
        exit( 1 )



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
