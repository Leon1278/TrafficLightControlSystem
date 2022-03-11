import traci
import numpy
import sys
import logging
import model.SimulationInformations as simInfo

logging.basicConfig(filename=f'{simInfo.OUTPUT_DIR}/{simInfo.LOGGING_FILENAME}.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')


# this class represents the implementation of the iTLM-Algorithm
class iTLM_Q_Algorithmus:

    def __init__(self, tlsInformationsClass):
        self.trafficLight = None
        self.prevDecision = None
        self.action = 0
        self.state = 0
        self.reward = 0
        self.learningRate = 0.5
        self.tlsInfos = tlsInformationsClass

    # function to translate a calculated decision into the corresponding sumo logic
    def __translateIntoSumoLogic(self, decision):

        sumoLogic = ""

        for i in range(len(decision)):
            value = decision[i]
            if value == 1:
                sumoLogic += "G"
            elif value == 0:
                sumoLogic += "r"
        return sumoLogic

    # function to modify a sumo logic into the corresponding yellow phase
    def __getYellowDecision(self, decision):

        tmp = decision.replace("G", "y")
        return tmp

    # main function inside the iTLM-Q Class which performs the actual calculation of a new decision
    def run(self, step, retQ, useLearning):

        aimVehiclesPerSecond = simInfo.AIM_VEHICLES_PER_SECOND
        lastArrivalDistance = 0
        arrivalDistance = None

        phaseDuration = self.trafficLight.phaseDuration
        self.reward = 0
        incSplit = self.trafficLight.initIncSplit()

        state_size = len(self.trafficLight.phases)
        action_size = len(self.trafficLight.phases)

        if retQ is not None:  # to reuse a q-table which was given to the method
            Q = retQ
        else:
            numpy.random.seed(79)
            Q = numpy.random.rand(state_size, action_size)
            Q = Q * 0.5  # q-table get initialized with random value between 0 and 0,5

        lst = self.trafficLight.phases  # list that contains every possible greenphase
        idl = self.trafficLight.incVehicles

        if len(idl.keys()) > 0:
            meanSpeedTmp = 0
            try:
                for edge in self.trafficLight.incEdges:
                    meanSpeedTmp += traci.edge.getLastStepMeanSpeed(edge)
                    meanSpeed = meanSpeedTmp / len(self.trafficLight.incEdges)
                    arrivalDistance = meanSpeed * (phaseDuration + 3)

                ####################################################
                # function call to modify the arrival distance
                # this is active when InVehSt Simulation is used
                if simInfo.IN_VEH_ST:
                    arrivalDistance = self.modifyArrivalDistance(self.trafficLight.incVehicles,self.trafficLight.nextIncVehicles, arrivalDistance)

            except Exception as e:
                print("Using default values due to error in mean speed calculation :", e)
                meanSpeed = 12
                arrivalDistance = meanSpeed * (phaseDuration + 3)

        for key in idl.keys():
            vehIDTmp = key  # id of the vehicle

            if step == self.trafficLight.secondYellowPhase:

                # distance function which rounds the exact distance to hundreds
                if simInfo.ANONYMITY_CLUSTERING:
                    distance = self.modifyDistanceForAnonymity(int(self.trafficLight.incVehicles.get(key).get("distance")), arrivalDistance)
                else:
                    distance = round(int(self.trafficLight.incVehicles.get(key).get("distance")))

                # compute distance in which every car gets across the trafficlight for the next Greenphase duration
                if vehIDTmp in self.trafficLight.incVehicles and distance < arrivalDistance:
                    incSplit = self.trafficLight.builtArray(vehIDTmp, incSplit)

                # computes the number of cars which passed the traffic light in the last green phase
                if traci.vehicle.getLanePosition(vehIDTmp) < lastArrivalDistance:
                    self.reward += 1
                lastArrivalDistance = arrivalDistance

        if step == self.trafficLight.secondYellowPhase:

            self.prevDecision = self.trafficLight.phase

            # Reward System for updating the q-table
            self.reward = self.reward / (phaseDuration * aimVehiclesPerSecond)
            newState = self.action

            if self.reward != 0:
                Q[self.state, self.action] = Q[self.state, self.action] + self.learningRate * (self.reward - Q[self.state, self.action])  # update formula for the q-table

            # algorithm to find the ultimate decision regarding every possibility
            maxIndex = 0
            maxValue = 0

            for i in range(len(lst)):
                tmpValue = 0
                for q in range(len(lst[i])):
                    if lst[i][q] == 1:
                        tmpIndex = i
                        qv = Q[newState, i]
                        if qv != 0.0 and useLearning == 1:  # checks if learning is wanted to be used
                            tmpValue += 10 * incSplit[q] + incSplit[
                                q] * qv  # calculates value for every possible greenphase
                        else:
                            tmpValue += 10 * incSplit[q]  # calculates value for every possible greenphase

                        if tmpValue > maxValue:
                            maxValue = tmpValue
                            maxIndex = tmpIndex

            self.trafficLight.decision = numpy.array(lst[maxIndex]) # the phase with the max value gets taken as decision
            self.action = maxIndex
            self.state = newState

            translated_decision = self.__translateIntoSumoLogic(self.trafficLight.decision)
            self.trafficLight.decision = translated_decision
            if translated_decision != self.prevDecision:
                yellowDec = self.__getYellowDecision(self.prevDecision)
                traci.trafficlight.setRedYellowGreenState(self.trafficLight.id, yellowDec)  # performs the new phase of the traffic light

            ####################################################
            # function call to modify the phase duration
            # this is active when InVehSt Simulation is used
            if simInfo.IN_VEH_ST:
                modifiedPhaseDuration = self.modifyTlsPhaseDuration(self.trafficLight.incVehicles, self.trafficLight.nextIncVehicles, 30)
                self.trafficLight.setPhaseDuration(modifiedPhaseDuration)

        if step == self.trafficLight.firstYellowPhase:
            if self.trafficLight.decision != self.prevDecision:
                yellowDec = self.__getYellowDecision(self.trafficLight.decision)
                traci.trafficlight.setRedYellowGreenState(self.trafficLight.id, yellowDec)  # performs the new phase of the traffic light

        if step == self.trafficLight.greenPhase:
            self.trafficLight.secondYellowPhase += phaseDuration + 6
            self.trafficLight.firstYellowPhase += phaseDuration + 6
            self.trafficLight.greenPhase += phaseDuration + 6
            traci.trafficlight.setRedYellowGreenState(self.trafficLight.id, self.trafficLight.decision)  # performs the new phase of the traffic light

        sys.stdout.flush()
        return Q, self.trafficLight.decision, arrivalDistance

    # function which handles the modulation of the distance from a vehicle to its upcoming tls
    # in a real situation this would be performed inside the vehicle itself and not inside the tls (chapter 6.5)
    def modifyDistanceForAnonymity(self, dist, arrivalDistance):

        quarter01 = arrivalDistance - dist
        quarter02 = arrivalDistance*2 - dist
        quarter03 = arrivalDistance*3 - dist
        quarter04 = arrivalDistance*4 - dist
        distMin = min(abs(quarter01), abs(quarter02), abs(quarter03), abs(quarter04))
        if distMin == abs(quarter01):
            dist = arrivalDistance * 0.8
        elif distMin == abs(quarter02):
            dist = arrivalDistance * 2
        elif distMin == abs(quarter03):
            dist = arrivalDistance * 3
        elif distMin == abs(quarter04):
            dist = arrivalDistance * 4
        return dist

    # function to modify the phase duration according to the incoming vehicles and the incoming vehicles at surrounding tls
    # only when incoming vehicles and incoming vehicles at surrounding tls are greater then 10 a modification is done
    # at lower traffic densities there is no effect measureable from the modification
    def modifyTlsPhaseDuration(self, incVehicles, nextIncVehicles, phaseDuration):

        if (len(incVehicles)) > 10 and len(nextIncVehicles) > 10:
            phaseDuration = round(phaseDuration * (1 + (len(nextIncVehicles) + len(incVehicles)) / 100))
        return phaseDuration

    # function to modify the arrival distance according to the incoming vehicles and the incoming vehicles at surrounding tls
    def modifyArrivalDistance(self, incVehicles, nextIncVehicles, arrivalDistance):

        arrDisTmp = arrivalDistance * (1 - (len(nextIncVehicles) + len(incVehicles)) / 1000)
        arrivalDistance = (arrivalDistance - arrDisTmp) * 3
        if arrivalDistance < 10:
            arrivalDistance = 10
        return arrivalDistance

    def setTrafficLight(self, trafficLight):
        self.trafficLight = trafficLight