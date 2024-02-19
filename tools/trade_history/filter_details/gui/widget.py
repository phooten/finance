# This Python file uses the following encoding: utf-8
import sys
import subprocess

from PySide6.QtWidgets import QApplication, QWidget

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


    def filterButtonPressed( self ):
        # TODO: Hardcoded for now
#        script_path = "/Users/phoot/code/finance/tools/trade_history/filter_details/test.py"
        script_path = "../test.py"
        argument = 99

        # Run the script "$(script path) -t1 ${argument}"
        command = "python3 " + script_path + " -t1 " + str( argument )

        subprocess.call( command, shell=True)
#        subprocess.call( "pwd", shell=True)


    def exitButtonPressed( self ):
        exit( 1 )



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
