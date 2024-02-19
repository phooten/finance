# This is a test for the GUI input / output from QT



import argparse


def setUpArguments():
    parser = argparse.ArgumentParser( description='input passed from QT Gui' )
    parser.add_argument('-t1', '--test_1', type=int, default=42, help='Enter a test value via the QT GUI')
    return vars( parser.parse_args() )

def main():
    arguments = setUpArguments()

    test_value = "N/A"
    print( "Test Value 1: " + str( arguments['test_1'] ) )
    return


if __name__ == "__main__":
    main()
