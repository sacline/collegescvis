#**collegescvis**

##Description

Python application for plotting and visualizing [College Scorecard] (https://collegescorecard.ed.gov) data.

###Current features:
* A [PyQt] (https://riverbankcomputing.com/software/pyqt/intro) interface using [Matplotlib] (matplotlib.org) to plot user-specified Scorecard data.
* Plots designed to easily compare different data types from different colleges over a range of years.
* Ability to export plotted data in JSON format.
* An sqlite3 database built from raw data is used to generate the plots.

###Future improvements:
* Move some of the command line input into the interface.
* Global settings file for specifying raw data file locations, etc. without having to modify source files.
* Additional customization options for plotted data.

##Requirements:
* Python 3.4+
* Matplotlib 1.4.2-3.1+
* PyQt4 4.11.2+
Please let me know if you have any trouble running the program, as well as the version of the above packages you are using.
