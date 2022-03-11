import xml.etree.ElementTree as ET
import pandas as pd
import argparse

"""

This script is used to calculate meanRunningVehicles and maxRunningVehicles. The returned xlsx file 
should then be added to Ergebnis_Übersicht_Summarys.xlsx.

USAGE: python computeSummary.py -f <input-filename> -o <output-filename>

"""


def get_options():

    filename = None
    outputfile = None

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--Help", help="Show usage")
    parser.add_argument("-f", "--Filename", help="Add input filename")
    parser.add_argument("-o", "--Outputfile", help="Add output filename")

    args = parser.parse_args()

    if args.Help:
        print("Usage : \n computeSummary.py -f <filename>.xml -o <outputfile>.xlsx")
    if args.Filename:
        filename = args.Filename
    if args.Outputfile:
        outputfile = args.Outputfile
    return filename, outputfile


def getSummaryStatistics(filename, outputfile):
    tree = ET.parse(f'{filename}.xml')
    root = tree.getroot()

    runningTotal = 0.0
    runningMax = 0
    counter = 0
    for child in root:

        collisions = float(child.attrib.get("collisions"))

        runningTmp = float(child.attrib.get("running"))
        runningTotal += runningTmp
        if runningTmp > runningMax:
            runningMax = runningTmp
        counter += 1

    runningAvg = runningTotal / counter

    statistics = {'meanRunningVehicles': [runningAvg], 'maxRunningVehicles': [runningMax], 'collisions': [collisions]}

    df = pd.DataFrame(statistics, columns=['meanRunningVehicles', 'maxRunningVehicles', 'collisions'])
    df.to_excel(f'{outputfile}.xlsx', index=False)


if __name__ == "__main__":
    filename, outputfile = get_options()
    print(filename, outputfile)
    getSummaryStatistics(filename, outputfile)