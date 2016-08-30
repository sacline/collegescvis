"""Main module for launching all CollegeSCVis unit tests.

Functions:
    main(): launch all unit tests.
"""
from test.test_dbbuilder import *
from test.test_decoder import *


def main():
    """Execute all unit tests."""
    unittest.main()

if __name__ == '__main__':
    main()
