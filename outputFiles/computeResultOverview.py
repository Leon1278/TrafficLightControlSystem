import matplotlib.pyplot as plt
import pandas as pd

"""

This Script is used to calculate bar plots from a xlsx or csv file. 
The required files are: 1. Result_Overview_Summary.xlsx and Result_Overview_Tripinfo.xlsx
or any other file that has the same shape and format

"""


class PlotEngine:

    def __init__(self):
        self.df = None

    def read_csv_file(self, filename, sheetName):

        file = pd.ExcelFile(filename)
        df = file.parse(sheetName)
        self.df = df

    def plot_meanRunningVehicles(self, title, saveName):

        fig, ax = plt.subplots()
        c_rects = plt.bar(self.df.Simulationsname, self.df.meanRunningVehicles, edgecolor='black', linewidth=1.2, color=['white', 'darkgrey', 'grey', 'black'], width=0.5)
        self.autolabel(c_rects, ax)
        plt.title(title)
        plt.xticks(rotation=90)
        plt.ylabel("Fahrzeuganzahl")
        plt.tight_layout()
        self.save_plot(saveName)
        plt.show()

    def plot_meanDuration(self, title, saveName):
        fig, ax = plt.subplots()
        c_rects = plt.bar(self.df.Simulationsname, self.df.duration, edgecolor='black', linewidth=1.2, color=['white', 'grey', 'black'], width=0.5)
        self.autolabel(c_rects, ax)
        plt.title(title)
        plt.xticks(rotation=90)
        plt.ylabel("(Simulations) Sekunde)")
        plt.tight_layout()
        self.save_plot(saveName)
        plt.show()

    def plot_meanWaitingTime(self, title, saveName):
        fig, ax = plt.subplots()
        c_rects = plt.bar(self.df.Simulationsname, self.df.meanWaitingTime, edgecolor='black', linewidth=1.2,
                          color=['white', 'grey', 'black'], width=0.5)
        self.autolabel(c_rects, ax)
        plt.title(title)
        plt.xticks(rotation=90)
        plt.ylabel("Simulationsschritt")
        plt.tight_layout()
        self.save_plot(saveName)
        plt.show()

    def save_plot(self, saveName):

        plt.savefig(saveName, format='pdf')

    def autolabel(self, rects, ax):

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., height - 0,
                    '%.1f' % float(height), ha='center', va='bottom', fontsize=7)


if __name__ == "__main__":

    plotEngine = PlotEngine()

    plotEngine.read_csv_file('Result_Overview_Summary.xlsx', 'Summarys')
    plotEngine.plot_meanRunningVehicles('Durchschnittliche Anzahl aktiver Fahrzeuge', 'Durchschnittliche_Fahrzeuganzahl.pdf')

    #plotEngine.read_csv_file('Result_Overview_Tripinfo.xlsx', 'Tripinfo')
    #plotEngine.plot_meanDuration('Durchschnittliche Durchlaufzeit','Durchschnittliche_Durchlaufzeit.pdf')
    #plotEngine.plot_meanWaitingTime('Durchschnittliche Wartezeit', 'Durchschnittliche_Wartezeit.pdf')

