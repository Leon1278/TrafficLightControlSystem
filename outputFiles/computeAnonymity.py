import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.colors import Normalize

""" 

This Script is used to generate three different anonymity plots from anonymity xml files.
Different configurations are possible to use different privacy level.

    # K -> which k shall be used
    # percentage -> percentage of incoming cars that need to achieve the choosen K value
    # NextTLS -> if set to true fourth quasi identifier nextTLS is considered (needed for the InVehSt to modify phase duration and arrival distance)
    # TLSIDS -> TLS Ids for which the calculation is made
    # VEHICLE_TRASHOLD -> determines the amount of active vehicles that is required to take a step into account
    # SAVE_PLOTS -> If set to True plots are saved

"""


def getAnonymityHistogramOriginalPercentage():

    # Configuration:
    ######################################

    K = 2
    percentage = 1
    NextTLS = False
    TLSIDS = ["cluster_277739062_39732718_89129091_89129092",
              "cluster_306484187_cluster_1200363791_1200363826_1200363834_1200363898_1200363927_1200363938_1200363947_1200364074_1200364103_1507566554_1507566556_255882157_306484190",
              "gneJ214"]

    tree = ET.parse("anonymity-1-InVehSt.xml")
    treeSummary = ET.parse('summary-1-InVehSt.xml')

    OUTPUT_FILENAME_ENDING = "1_InVehSt"
    VEHICLE_TRASHOLD = 2500
    SAVE_PLOTS = True

    #######################################

    root = tree.getroot()
    rootSummary = treeSummary.getroot()

    min_k_one_dist = []
    k_perc_two_dist = []
    min_k_two_dist = []
    k_perc_three_dist = []
    min_k_three_dist = []
    k_perc_four_dist = []
    min_k_four_dist = []
    k_perc_five_dist = []
    min_k_five_dist = []

    min_k_one_edgeInc = []
    k_perc_two_edgeInc = []
    min_k_two_edgeInc = []
    k_perc_three_edgeInc = []
    min_k_three_edgeInc = []
    k_perc_four_edgeInc = []
    min_k_four_edgeInc = []
    k_perc_five_edgeInc = []
    min_k_five_edgeInc = []

    min_k_one_edgeOut = []
    k_perc_two_edgeOut = []
    min_k_two_edgeOut = []
    k_perc_three_edgeOut = []
    min_k_three_edgeOut = []
    k_perc_four_edgeOut = []
    min_k_four_edgeOut = []
    k_perc_five_edgeOut = []
    min_k_five_edgeOut = []

    min_k_one_tls = []
    k_perc_two_tls = []
    min_k_two_tls = []
    k_perc_three_tls = []
    min_k_three_tls = []
    k_perc_four_tls = []
    min_k_four_tls = []
    k_perc_five_tls = []
    min_k_five_tls = []

    step = []
    counter = 0
    for child in root:
        if child.tag == "anonymity-percentage":
            if TLSIDS is not None:
                if child.attrib.get("tlsid") in TLSIDS:

                    # below code section can be uncomment and then used to only use childs from root file where
                    # the corresponding step inside the summary file is higher then the specified trashhold

                    stepStr = child.attrib.get("step")
                    stepTmpAnonymity = int(stepStr) / 10
                    print("Step Anonymity :", stepTmpAnonymity)
                    for childSummary in rootSummary:
                        stepSummaryTmp = childSummary.attrib.get("time")
                        if float(stepSummaryTmp) == float(stepTmpAnonymity):
                            runningVehicles = int(childSummary.attrib.get("running"))
                            if runningVehicles > VEHICLE_TRASHOLD:

                                k_perc_two_dist_tmp = child.attrib.get("k_two_perc_dist")
                                k_perc_two_dist.append(float(k_perc_two_dist_tmp))
                                if float(k_perc_two_dist_tmp) == 1.0:
                                    min_k_two_dist.append(2)

                                k_perc_three_dist_tmp = child.attrib.get("k_three_perc_dist")
                                k_perc_three_dist.append(float(k_perc_three_dist_tmp))
                                if float(k_perc_three_dist_tmp) == 1.0:
                                    min_k_three_dist.append(3)

                                k_perc_four_dist_tmp = child.attrib.get("k_four_perc_dist")
                                k_perc_four_dist.append(float(k_perc_four_dist_tmp))
                                if float(k_perc_four_dist_tmp) == 1.0:
                                    min_k_four_dist.append(4)

                                k_perc_five_dist_tmp = child.attrib.get("k_five_perc_dist")
                                k_perc_five_dist.append(float(k_perc_five_dist_tmp))
                                if float(k_perc_five_dist_tmp) == 1.0:
                                    min_k_five_dist.append(5)


                                min_k_one_dist.append(1)

                                ##############################################################

                                k_perc_two_edgeInc_tmp = child.attrib.get("k_two_perc_edgeInc")
                                k_perc_two_edgeInc.append(float(k_perc_two_edgeInc_tmp))
                                if float(k_perc_two_edgeInc_tmp) == 1.0:
                                    min_k_two_edgeInc.append(2)

                                k_perc_three_edgeInc_tmp = child.attrib.get("k_three_perc_edgeInc")
                                k_perc_three_edgeInc.append(float(k_perc_three_edgeInc_tmp))
                                if float(k_perc_three_edgeInc_tmp) == 1.0:
                                    min_k_three_edgeInc.append(3)

                                k_perc_four_edgeInc_tmp = child.attrib.get("k_four_perc_edgeInc")
                                k_perc_four_edgeInc.append(float(k_perc_four_edgeInc_tmp))
                                if float(k_perc_four_edgeInc_tmp) == 1.0:
                                    min_k_four_edgeInc.append(4)

                                k_perc_five_edgeInc_tmp = child.attrib.get("k_five_perc_edgeInc")
                                k_perc_five_edgeInc.append(float(k_perc_five_edgeInc_tmp))
                                if float(k_perc_five_edgeInc_tmp) == 1.0:
                                    min_k_five_edgeInc.append(5)

                                min_k_one_edgeInc.append(1)

                                ##############################################################

                                k_perc_two_edgeOut_tmp = child.attrib.get("k_two_perc_edgeOut")
                                k_perc_two_edgeOut.append(float(k_perc_two_edgeOut_tmp))
                                if float(k_perc_two_edgeOut_tmp) == 1.0:
                                    min_k_two_edgeOut.append(2)

                                k_perc_three_edgeOut_tmp = child.attrib.get("k_three_perc_edgeOut")
                                k_perc_three_edgeOut.append(float(k_perc_three_edgeOut_tmp))
                                if float(k_perc_three_edgeOut_tmp) == 1.0:
                                    min_k_three_edgeOut.append(3)

                                k_perc_four_edgeOut_tmp = child.attrib.get("k_four_perc_edgeOut")
                                k_perc_four_edgeOut.append(float(k_perc_four_edgeOut_tmp))
                                if float(k_perc_four_edgeOut_tmp) == 1.0:
                                    min_k_four_edgeOut.append(4)

                                k_perc_five_edgeOut_tmp = child.attrib.get("k_five_perc_edgeOut")
                                k_perc_five_edgeOut.append(float(k_perc_five_edgeOut_tmp))
                                if float(k_perc_five_edgeOut_tmp) == 1.0:
                                    min_k_five_edgeOut.append(5)

                                min_k_one_edgeOut.append(1)

                                ##############################################################

                                k_perc_two_tls_tmp = child.attrib.get("k_two_perc_tls")
                                k_perc_two_tls.append(float(k_perc_two_tls_tmp))
                                if float(k_perc_two_tls_tmp) == 1.0:
                                    min_k_two_tls.append(2)

                                k_perc_three_tls_tmp = child.attrib.get("k_three_perc_tls")
                                k_perc_three_tls.append(float(k_perc_three_tls_tmp))
                                if float(k_perc_three_tls_tmp) == 1.0:
                                    min_k_three_tls.append(3)

                                k_perc_four_tls_tmp = child.attrib.get("k_four_perc_tls")
                                k_perc_four_tls.append(float(k_perc_four_tls_tmp))
                                if float(k_perc_four_tls_tmp) == 1.0:
                                    min_k_four_tls.append(4)

                                k_perc_five_tls_tmp = child.attrib.get("k_five_perc_tls")
                                k_perc_five_tls.append(float(k_perc_five_tls_tmp))
                                if float(k_perc_five_tls_tmp) == 1.0:
                                    min_k_five_tls.append(5)

                                min_k_one_tls.append(1)

                                ################################################################

                                if K == 2:
                                    if NextTLS:
                                        if float(k_perc_two_dist_tmp) >= percentage and float(k_perc_two_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage and float(k_perc_two_tls_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                    else:
                                        if float(k_perc_two_dist_tmp) >= percentage and float(k_perc_two_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                elif K == 3:
                                    if NextTLS:
                                        if float(k_perc_three_dist_tmp) >= percentage and float(k_perc_three_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage and float(k_perc_three_tls_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                    else:
                                        if float(k_perc_three_dist_tmp) >= percentage and float(k_perc_three_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                elif K == 4:
                                    if NextTLS:
                                        if float(k_perc_four_dist_tmp) >= percentage and float(k_perc_four_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage and float(k_perc_four_tls_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                    else:
                                        if float(k_perc_four_dist_tmp) >= percentage and float(k_perc_four_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                elif K == 5:
                                    if NextTLS:
                                        if float(k_perc_five_dist_tmp) >= percentage and float(k_perc_five_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage and float(k_perc_five_tls_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                    else:
                                        if float(k_perc_five_dist_tmp) >= percentage and float(k_perc_five_edgeInc_tmp) >= percentage and float(
                                                k_perc_two_edgeOut_tmp) >= percentage:
                                            step.append(child.attrib.get("step"))
                                counter += 1
                            break

    ############################# FIRST GRAPH ###################################

    min_k_dist = min_k_one_dist + min_k_two_dist + min_k_three_dist + min_k_four_dist + min_k_five_dist
    min_k_edgeInc = min_k_one_edgeInc + min_k_two_edgeInc + min_k_three_edgeInc + min_k_four_edgeInc + min_k_five_edgeInc
    min_k_edgeOut = min_k_one_edgeOut + min_k_two_edgeOut + min_k_three_edgeOut + min_k_four_edgeOut + min_k_five_edgeOut
    min_k_tls = min_k_one_tls + min_k_two_tls + min_k_three_tls + min_k_four_tls + min_k_five_tls

    fig, axs = plt.subplots(1, 4, sharey=True)
    bins = np.arange(7) - 0.5

    N, bins, patches = axs[0].hist(min_k_dist, edgecolor='black', linewidth=1.2, color=['grey'], bins=bins)
    axs[0].set_title("Distanz zum \n TLS", fontsize=9)
    axs[0].set_xticks(range(6))
    axs[0].set_ylabel("Häufigkeit")
    axs[0].set_xlim([0, 6])

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    N, bins, patches = axs[1].hist(min_k_edgeInc, edgecolor='black', linewidth=1.2, color=['grey'], bins=bins)
    axs[1].set_title("Eingehende \n Straße", fontsize=9)
    axs[1].set_xticks(range(6))
    axs[1].set_xlim([0, 6])

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    N, bins, patches = axs[2].hist(min_k_edgeOut, edgecolor='black', linewidth=1.2, color=['grey'], bins=bins)
    axs[2].set_title("Ausgehende \n Straße", fontsize=9)
    axs[2].set_xticks(range(6))
    axs[2].set_xlim([0, 6])

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    N, bins, patches = axs[3].hist(min_k_tls, edgecolor='black', linewidth=1.2, color=['grey'], bins=bins)
    axs[3].set_title("Übernächstes \n TLS", fontsize=9)
    axs[3].set_xticks(range(6))
    axs[3].set_xlim([0, 6])

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("k-Anonymität")
    fig.tight_layout()
    if SAVE_PLOTS:
        plt.savefig(f'k{K}Distribution_{OUTPUT_FILENAME_ENDING}.pdf', format='pdf')
    plt.show()

    ############################# SECOND GRAPH ###################################

    if K == 2:
        used_dist = k_perc_two_dist
        used_edgeInc = k_perc_two_edgeInc
        used_edgeOut = k_perc_two_edgeOut
        used_tls = k_perc_two_tls
    elif K == 3:
        used_dist = k_perc_three_dist
        used_edgeInc = k_perc_three_edgeInc
        used_edgeOut = k_perc_three_edgeOut
        used_tls = k_perc_three_tls
    elif K == 4:
        used_dist = k_perc_four_dist
        used_edgeInc = k_perc_four_edgeInc
        used_edgeOut = k_perc_four_edgeOut
        used_tls = k_perc_four_tls
    elif K == 5:
        used_dist = k_perc_five_dist
        used_edgeInc = k_perc_five_edgeInc
        used_edgeOut = k_perc_five_edgeOut
        used_tls = k_perc_five_tls
    else:
        used_dist = k_perc_two_dist
        used_edgeInc = k_perc_two_edgeInc
        used_edgeOut = k_perc_two_edgeOut
        used_tls = k_perc_two_tls

    fig, axs = plt.subplots(1, 4, sharey=True)

    bins = np.arange(0, 1.2, 0.1) - 0.05
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    N, bins, patches = axs[0].hist(used_dist, edgecolor='black', linewidth=1.2, bins=bins)
    axs[0].set_title(f'Prozentuale \n Anonymität k >={K} \n Distanz', fontsize=9)
    axs[0].set_xticks(x)
    axs[0].set_ylabel("Häufigkeit")
    axs[0].set_xticklabels(x, fontsize=5, rotation='vertical')

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    N, bins, patches = axs[1].hist(used_edgeInc, edgecolor='black', linewidth=1.2, color=['grey'], bins=bins)
    axs[1].set_title(f'Prozentuale \n Anonymität k >={K} \n Eingehende Straße', fontsize=9)
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(x, fontsize=5, rotation='vertical')

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    N, bins, patches = axs[2].hist(used_edgeOut, edgecolor='black', linewidth=1.2, color=['grey'], bins=bins)
    axs[2].set_title(f'Prozentuale \n Anonymität k >={K} \n Ausgehende Straße', fontsize=9)
    axs[2].set_xticks(x)
    axs[2].set_xticklabels(x, fontsize=5, rotation='vertical')

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    N, bins, patches = axs[3].hist(used_tls, edgecolor='black', linewidth=1.2, color=['grey'], bins=bins)
    axs[3].set_title(f'Prozentuale \n Anonymität k >={K} \n übernächstes TLS', fontsize=9)
    axs[3].set_xticks(x)
    axs[3].set_xticklabels(x, fontsize=5, rotation='vertical')

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Fahrzeuganteil mit k-Anonymität")
    fig.tight_layout()
    if SAVE_PLOTS:
        plt.savefig(f'PercDistributionK{K}_{OUTPUT_FILENAME_ENDING}.pdf', format='pdf')
    plt.show()

    ############################# THIRD GRAPH ###################################

    labels = f'k>={K}', f'k<{K}'
    colors = ['#c6f5a7', '#f6ccb9']
    stepAnonym = len(step)
    stepCount = counter - len(step)
    metrics = [stepAnonym, stepCount]
    explode = (0, 0)
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.pie(metrics, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
           wedgeprops={"edgecolor": "black", 'linewidth': 0.8}, textprops={'fontsize': 7})
    ax.axis('equal')
    fig.tight_layout()
    if SAVE_PLOTS:
        plt.savefig(f'TotalAchievedAnonymityK{K}_{OUTPUT_FILENAME_ENDING}.pdf', format='pdf')
    plt.show()


if __name__ == "__main__":
    getAnonymityHistogramOriginalPercentage()
