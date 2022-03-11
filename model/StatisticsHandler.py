import collections
import logging
from lxml import etree as ET
import model.SimulationInformations as simInfo

logging.basicConfig(filename=f'{simInfo.OUTPUT_DIR}/{simInfo.LOGGING_FILENAME}.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')


# class to calculate the count per phase duration aswell as the reached k-anonymity level
# the count per phaseduration
class StatisticsHandler:

    def __init__(self, trafficlightIds):
        self.statistics = {}
        self.prevIncVehicles = {}
        for tlsId in trafficlightIds:
            self.prevIncVehicles[tlsId.get("id")] = {}
        self.counts = {}
        for tlsId in trafficlightIds:
            self.counts[tlsId.get("id")] = 0
        self.indexCounter = 0
        self.rootStatistics = ET.Element("statistics")
        self.rootAnonymity = ET.Element("anonymity")
        self.rootAnonymityPercentage = ET.Element("anonymity-percentage")

    def getVehiclesPerPhaseDuration(self, tlsId, incVehicles, prevIncVehicles, step, secondYellowPhase):
        # calculates amount of vehicles that passed the TLS last phase duration
        # this calculation will only be executed if the TLS id is configured inside the SimulationInformations class
        # this is done by comparing the previous incoming vehicles with the actual incoming vehicles

        if tlsId in simInfo.TLSIDS_STATISTICS:
            count = self.counts.get(tlsId)
            setOfIncVehicles = set(incVehicles)
            setOfPrevIncVehicles = set(prevIncVehicles)
            differences = setOfIncVehicles ^ setOfPrevIncVehicles
            for diff in differences:
                if diff not in incVehicles:
                    count += 1
            self.counts[tlsId] = count
            if secondYellowPhase == step:
                self.writeToXml(tlsId, str(count), str(step))
                self.counts[tlsId] = 0

    def modifyDistanceForAnonymity(self, dist, arrivalDistance):
        # as in the TrafficLightSystem class the distance from a vehicle to the upcoming TLS is modified
        # this modification has a big impact on the reachable privacy level (chapter 6.5)

        tmp250 = arrivalDistance - dist
        tmp500 = arrivalDistance * 2 - dist
        tmp750 = arrivalDistance * 3 - dist
        tmp1000 = arrivalDistance * 4 - dist
        distMin = min(abs(tmp250), abs(tmp500), abs(tmp750), abs(tmp1000))
        if distMin == abs(tmp250):
            dist = arrivalDistance * 0.8
        elif distMin == abs(tmp500):
            dist = arrivalDistance * 2
        elif distMin == abs(tmp750):
            dist = arrivalDistance * 3
        elif distMin == abs(tmp1000):
            dist = arrivalDistance * 4
        return dist

    def getAmountPerQuasiIdentifier(self, tlsId, tls, step, arrivalDistance):
        # function that counts the occurences of every element inside a list
        # in the end there is for every quasi identifer a list that contains the count of occurences
        # for every element e.q. for distance {"300":3, "200":5, ...} <-- 3 and 5 are
        # the keys used inside getPercentage()

        if tlsId in simInfo.TLSIDS_STATISTICS:
            actualEdges = tls.actualEdges
            nextEdges = tls.nextEdges
            incVehicles = tls.incVehicles
            distances = []
            incEdges = []
            outEdges = []
            nextTls = []
            if incVehicles is not None:
                if len(incVehicles) > 0:
                    for key in incVehicles.keys():
                        incVehicle = incVehicles.get(key)
                        dist = int(incVehicle.get("distance"))
                        if arrivalDistance is not None:
                            if simInfo.ANONYMITY_CLUSTERING:
                                dist = self.modifyDistanceForAnonymity(dist, arrivalDistance)
                            else:
                                dist = round(int(incVehicle.get("distance")))
                        else:
                            dist = round(dist / 100) * 100
                        distances.append(dist)
                        nextTlsTmp = incVehicle.get("nextTls")
                        nextTls.append(nextTlsTmp)
                        incEdge = actualEdges.get(key)
                        splittedEdgInc = str(incEdge).split('#')
                        incEdges.append(splittedEdgInc[0])
                        outEdge = nextEdges.get(key)
                        splittedEdgOut = str(outEdge).split('#')
                        outEdges.append(splittedEdgOut[0])

                    occurencesDist = collections.Counter(distances)
                    occurencesEdgInc = collections.Counter(incEdges)
                    occurencesEdgOut = collections.Counter(outEdges)
                    occurencesNextTls = collections.Counter(nextTls)

                    if len(occurencesDist) > 0 and len(occurencesEdgInc) > 0 and len(occurencesEdgOut) > 0 and len(nextTls) > 0:

                        k_two_perc_dist, k_three_perc_dist, k_four_perc_dist, k_five_perc_dist = self.getPercentage(occurencesDist)
                        k_two_perc_edgeInc, k_three_perc_edgeInc, k_four_perc_edgeInc, k_five_perc_edgeInc = self.getPercentage(occurencesEdgInc)
                        k_two_perc_edgeOut, k_three_perc_edgeOut, k_four_perc_edgeOut, k_five_perc_edgeOut = self.getPercentage(occurencesEdgOut)
                        k_two_perc_tls, k_three_perc_tls, k_four_perc_tls, k_five_perc_tls = self.getPercentage(occurencesNextTls)
                        self.writeToXmlKAnonymityPercentage(tlsId, str(k_two_perc_dist), str(k_three_perc_dist), str(k_four_perc_dist), str(k_five_perc_dist),
                                                            str(k_two_perc_edgeInc), str(k_three_perc_edgeInc), str(k_four_perc_edgeInc),
                                                            str(k_five_perc_edgeInc), str(k_two_perc_edgeOut), str(k_three_perc_edgeOut), str(k_four_perc_edgeOut),
                                                            str(k_five_perc_edgeOut), str(k_two_perc_tls), str(k_three_perc_tls),
                                                            str(k_four_perc_tls), str(k_five_perc_tls),str(step))

    def getPercentage(self, occurences):

        total = len(occurences)
        countTwo = 0
        countThree = 0
        countFour = 0
        countFive = 0
        for key in occurences.values():
            if key >= 2:
                countTwo += 1
            if key >= 3:
                countThree += 1
            if key >= 4:
                countFour += 1
            if key >= 5:
                countFive += 1

        k_two_perc = countTwo / total
        k_three_perc = countThree / total
        k_four_perc = countFour / total
        k_five_perc = countFive / total

        return k_two_perc, k_three_perc, k_four_perc, k_five_perc

    def writeToXmlKAnonymityPercentage(self, tlsId, k_two_perc_dist, k_three_perc_dist, k_four_perc_dist, k_five_perc_dist,
                                       k_two_perc_edgeInc, k_three_perc_edgeInc, k_four_perc_edgeInc, k_five_perc_edgeInc,
                                       k_two_perc_edgeOut, k_three_perc_edgeOut, k_four_perc_edgeOut, k_five_perc_edgeOut,
                                       k_two_perc_tls, k_three_perc_tls, k_four_perc_tls, k_five_perc_tls, step):

        element = ET.Element("anonymity-percentage", tlsid=tlsId, k_two_perc_dist=k_two_perc_dist, k_three_perc_dist=k_three_perc_dist,
                             k_four_perc_dist=k_four_perc_dist, k_five_perc_dist=k_five_perc_dist, k_two_perc_edgeInc=k_two_perc_edgeInc,
                             k_three_perc_edgeInc=k_three_perc_edgeInc, k_four_perc_edgeInc=k_four_perc_edgeInc, k_five_perc_edgeInc=k_five_perc_edgeInc,
                             k_two_perc_edgeOut=k_two_perc_edgeOut, k_three_perc_edgeOut=k_three_perc_edgeOut, k_four_perc_edgeOut=k_four_perc_edgeOut,
                             k_five_perc_edgeOut=k_five_perc_edgeOut, k_two_perc_tls=k_two_perc_tls, k_three_perc_tls=k_three_perc_tls,
                             k_four_perc_tls=k_four_perc_tls, k_five_perc_tls=k_five_perc_tls, step=step)

        self.rootAnonymityPercentage.append(element)
        self.indexCounter += 1
        tree = ET.ElementTree(self.rootAnonymityPercentage)
        tree.write(f'{simInfo.OUTPUT_DIR}/{simInfo.ANONYMITY_FILENAME}-percentage.xml', pretty_print=True)

    def writeToXml(self, tlsId, countPerPhaseDuration, step):

        element = ET.Element("statistic", tlsid=tlsId, countPerPhaseDuration=countPerPhaseDuration, step=step)
        self.rootStatistics.append(element)
        self.indexCounter += 1
        tree = ET.ElementTree(self.rootStatistics)
        tree.write(f'{simInfo.OUTPUT_DIR}/{simInfo.STATISTICS_FILENAME}.xml', pretty_print=True)

    def getPrevIncVehicles(self, tlsid):
        return self.prevIncVehicles.get(tlsid)

    def setPrevIncVehicles(self, tlsId, incVehicles):
        self.prevIncVehicles[tlsId] = incVehicles
