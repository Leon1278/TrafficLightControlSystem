import xml.etree.ElementTree as ET
import pandas as pd
import argparse

"""

This script is used to calculate meanWaitingTime and meanDuration. The returned xlsx file 
should then be added to Result_Overview_Tripinfo.xlsx.

USAGE: python computeTripinfo.py -f <input-filename> -o <output-filename>

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


def getTripinfoStatistics(filename, outputfile):
    tree = ET.parse(f'{filename}.xml')
    root = tree.getroot()

    waitingTimeTotal = 0.0
    waitingCountTotal = 0.0
    durationTotal = 0.0
    timeLossTotal = 0.0
    biggestWaitingTime = 0
    counter = 0
    for child in root:
        if child.tag == "tripinfo":

            durationTmp = child.attrib.get("duration")
            durationTotal += float(durationTmp)

            waitingTimeTmp = child.attrib.get("waitingTime")
            if float(waitingTimeTmp) > biggestWaitingTime:
                biggestWaitingTime = float(waitingTimeTmp)
            waitingTimeTotal += float(waitingTimeTmp)

            waitingCountTmp = child.attrib.get("waitingCount")
            waitingCountTotal += float(waitingCountTmp)

            timeLossTmp = child.attrib.get("timeLoss")
            timeLossTotal += float(timeLossTmp)

            counter += 1

    meanWaitingTime = waitingTimeTotal / counter
    meanWaitingCount = waitingCountTotal / counter
    meanDuration = durationTotal / counter
    meanTimeLoss = timeLossTotal / counter

    statistics = {'meanWaitingTime': [meanWaitingTime], 'meanWaitingCount': [meanWaitingCount],
                  'meanDuration': [meanDuration], 'meanTimeLoss': [meanTimeLoss]}

    df = pd.DataFrame(statistics, columns=['meanWaitingTime', 'meanWaitingCount', 'meanDuration', 'meanTimeLoss'])
    df.to_excel(f'{outputfile}.xlsx', index=False)


if __name__ == "__main__":
    filename, outputfile = get_options()
    print(filename, outputfile)
    getTripinfoStatistics(filename, outputfile)
