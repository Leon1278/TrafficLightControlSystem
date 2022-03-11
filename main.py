import itertools
import os
import sys
import sumolib
import logging
import traci

from model.TrafficLightInitializer import TrafficLightInitializer
from model.TrafficLightSystemInformations import TrafficLightSystemInformations
from model.iTLM_Q_Algorithmus import iTLM_Q_Algorithmus
from model.StatisticsHandler import StatisticsHandler
import model.SimulationInformations as simInfo

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

logging.basicConfig(filename=f'{simInfo.OUTPUT_DIR}/{simInfo.LOGGING_FILENAME}.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

trafficLightIds = simInfo.TRAFFIC_LIGHT_IDS


# function that runs the simulation and coordinates the different classes used inside the simulation
def simulation():

    logging.info("Starting pre initializing process...")

    net = sumolib.net.readNet('data/scenario/ingolstadt.net.xml')
    step = 0  # variable for iterating through the simulation

    # initlialize all classes that are needed
    tlsInformationsClass = TrafficLightSystemInformations(net)
    iTLM_Q = iTLM_Q_Algorithmus(tlsInformationsClass)
    tlsInitializer = TrafficLightInitializer(net, step, tlsInformationsClass, trafficLightIds)

    # initialize all possible decisions for the controlled traffic light systems
    tlsPhases = {}
    for trafficlightId in trafficLightIds:
        tlsPhase = getTlsPhase(trafficlightId.get("id"), tlsInformationsClass, trafficlightId.get("phase"))
        tlsPhases[trafficlightId.get("id")] = tlsPhase

    # initialize the actual timestamp for every traffic light system that is controlled
    tlTimestamps = {}
    for trafficlightId in trafficLightIds:
        tlTimestamps[trafficlightId.get("id")] = 90

    Q = None

    logging.info("Simulation started")

    """execute the TraCI control loop"""
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()  # performs one simulation step at a time

        # this function iterates through all vehicles and determine to which tls it is heading
        tlsInitializer.setVehiclesPerTls()

        # for every controlled tls several steps are executed
        # 1. the tls initializer class inits the next step for the tls
        # 2. the iTLM-Q Algorithm class performs the decision calculation
        # 3. Inside the tlsInformationClass all necessary informations are stored like the updated arrivalDistance,
        #    decision and q table (tlsInformationClass acts as in Simulation storage)
        for trafficlightId in trafficLightIds:

            tlsInitializer.setTlsId(trafficlightId.get("id"))
            tlsInitializer.setStep(step)
            tlsInitializer.setTlsPhases(tlsPhases[trafficlightId.get("id")])
            usedTls = tlsInitializer.initNextStep()
            iTLM_Q.setTrafficLight(usedTls)
            if step != 0:
                Q = tlsInformationsClass.getQTable(trafficlightId.get("id"))
            Q, decision, arrivalDistance = iTLM_Q.run(step, Q, 1)
            tlsInformationsClass.setArrivalDistance(trafficlightId.get("id"), arrivalDistance)
            tlsInformationsClass.setTlsDecision(trafficlightId.get("id"), decision)
            tlsInformationsClass.setQTable(trafficlightId.get("id"), Q)

        if step % 1000 == 0:
            logging.info("Step : %s", str(step))
        step += 1

    logging.info("Simualtion ended")

    traci.close()
    sys.stdout.flush()

# function to run the default simulation without any modification or control sequences
def defaultSimulation():

    logging.info("Simulation started at")
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if step % 1000 == 0:
            logging.info("Step : %s", str(step))
        step += 1
    traci.close()
    sys.stdout.flush()
    logging.info("Simualtion ended")


# function to run the default simulation with statistics for count per phase duration and k-anonymity
def defaultSimulationWithStatistics():

    net = sumolib.net.readNet('data/scenario/ingolstadt.net.xml')
    logging.info("Simulation started at")
    step = 0
    statisticsHandler = StatisticsHandler(trafficLightIds)
    phaseDuration = 30
    secondYellowPhase = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        tlsIds = net.getTrafficLights()
        idl = traci.vehicle.getIDList()
        vehiclesPerTls = {}
        try:
            for tlsId in tlsIds:
                vehiclesPerTls[tlsId._id] = {}
            for i in range(len(idl)):
                vehIDTmp = idl[i]
                if len(traci.vehicle.getNextTLS(vehIDTmp)) > 0:
                    tlsVehData = traci.vehicle.getNextTLS(vehIDTmp)
                    tmp = vehiclesPerTls[tlsVehData[0][0]]
                    tmp[vehIDTmp] = tlsVehData[0][2]
        except Exception:
            logging.error("Error while compute vehicles per TLS")
            logging.exception("Error-Message: ")

        for tls in trafficLightIds:
            statisticsHandler.getVehiclesPerPhaseDuration(tls.get("id"), vehiclesPerTls.get(tls.get("id")), statisticsHandler.getPrevIncVehicles(tls.get("id")), step, secondYellowPhase)
            statisticsHandler.setPrevIncVehicles(tls.get("id"), vehiclesPerTls.get(tls.get("id")))
        if secondYellowPhase == step:
            secondYellowPhase += phaseDuration + 6
        if step % 1000 == 0:
            logging.info("Step : %s", str(step))
        step += 1
    traci.close()
    sys.stdout.flush()
    logging.info("Simualtion ended")


# this function calculates the count per phase duration
# for that every step is checked which vehicles are no longer contained inside the array for incoming vehicles
# every secondYellowPhase (phase in which a new decision is calculated) the count is set to 0
def getVehiclesPerPhaseDuration(vehicles, prevVehicles, vehicleCount, step, secondYellowPhase):

    if len(prevVehicles) > 0:
        for vehicleId in prevVehicles:
            if not vehicleId in vehicles:
                vehicleCount += 1
    if step == secondYellowPhase:
        vehicleCount = 0
    prevVehicles = vehicles
    return vehicleCount, prevVehicles

# this function calculates all possible decisions for one tls
# for this an array which determines contradicting decisions is used
def getTlsPhase(tlsid, tlsInformations, tlsPhaseLength=19):

    lst = [list(i) for i in itertools.product([0, 1], repeat=tlsPhaseLength)]
    lstCopy = lst[:]
    contra = tlsInformations.contradictingTlsSignals.get(tlsid)
    try:
        for phase in lstCopy:
            removePhase = False
            switchPhase = False
            counter = 0
            while not removePhase and not switchPhase:
                for i in range(len(phase)):
                    counter += 1
                    if phase[i] == 1:
                        for con in contra[i]:
                            if phase[con] == 1:
                                removePhase = True
                                break
                    if counter >= tlsPhaseLength:
                        switchPhase = True
                    if removePhase:
                        break
            if removePhase:
                lst.remove(phase)
        logging.info('Finished generating phases for TLS : %s', str(tlsid))
    except Exception:
        logging.error('Error while generating tls phase list for TLS : %s', str(tlsid))
        logging.exception('Error-Message: ')
    return lst


if __name__ == "__main__":

    if simInfo.GUI:
        traci.start(['sumo-gui', "-c", "data/scenario/InTAS_full_poly.sumocfg", "--time-to-teleport", "-1", "--summary", f'{simInfo.OUTPUT_DIR}/{simInfo.SUMMARY_FILENAME}.xml', "--tripinfo-output", f'{simInfo.OUTPUT_DIR}/{simInfo.TRIPINFO_FILENAME}.xml'])
    elif not simInfo.GUI:
        if simInfo.SCALE == 0:
            traci.start(['sumo', "-c", "data/scenario/InTAS_full_poly.sumocfg", "--time-to-teleport", "-1", "--summary", f'{simInfo.OUTPUT_DIR}/{simInfo.SUMMARY_FILENAME}.xml', "--tripinfo-output", f'{simInfo.OUTPUT_DIR}/{simInfo.TRIPINFO_FILENAME}.xml'])
        else:
            traci.start(['sumo', "--scale", f'{simInfo.SCALE}', "-c", "data/scenario/InTAS_full_poly.sumocfg", "--time-to-teleport", "-1", "--summary", f'{simInfo.OUTPUT_DIR}/{simInfo.SUMMARY_FILENAME}.xml', "--tripinfo-output", f'{simInfo.OUTPUT_DIR}/{simInfo.TRIPINFO_FILENAME}.xml'])

    if simInfo.SIMULATION_TYPE == "simulation":
        simulation()
    elif simInfo.SIMULATION_TYPE == "defaultSimulation" and simInfo.GENERATE_STATISTICS:
        defaultSimulationWithStatistics()
    elif simInfo.SIMULATION_TYPE == "defaultSimulation" and not simInfo.GENERATE_STATISTICS:
        defaultSimulation()
