import traci
import logging
import copy

from model.StatisticsHandler import StatisticsHandler
from model.TrafficLightSystem import TrafficLightSystem
import model.SimulationInformations as simInfo

logging.basicConfig(filename=f'{simInfo.OUTPUT_DIR}/{simInfo.LOGGING_FILENAME}.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')


# this class is used to manage multiple inctances of the TrafficLightSystem class
class TrafficLightInitializer:

    def __init__(self, net, step, tlsInformationClass, trafficlightIds):
        self.net = net
        self.tlsId = None
        self.TLS = net.getTrafficLights()
        self.step = step
        self.tlsInformationsClass = tlsInformationClass
        self.defaultDecisions = {"30965809": "rrrrrrrrrrr", "cluster_21532613_25633348": "", "cluster_1443568606_1834131515_1834131519_1834131548_1834131550": "rrrrrrrrrrrrrrrrrrr", "gneJ214": "rrrrrrrrrrr", "214620430": "rrrrrrrrrrrrrrrr"}
        self.tlTimestamps = self.__initTlsTimestamps()
        self.vehiclesPerTls = {}
        self.nextVehiclesPerTls = {}
        self.vehiclesPerTlsModel = {}
        self.nextVehiclesPerTlsModel = {}
        for tls in self.TLS:
            self.vehiclesPerTlsModel[tls._id] = {}
            self.nextVehiclesPerTlsModel[tls._id] = {}
        self.setVehiclesPerTls()
        self.tlsPhases = None
        self.tls = self.preInitProcess(trafficlightIds)
        self.statisticsHandler = StatisticsHandler(trafficlightIds)

    def preInitProcess(self, trafficlightIds):
        # function to initialize instances of the TrafficLightSystem class for every
        # controlled traffic light system
        # is called right at the start of the simulation

        tlsList = {}
        try:
            for trafficlightId in trafficlightIds:
                tlsRaw = self.net.getTLS(trafficlightId.get("id"))
                tls = TrafficLightSystem(tlsRaw, self.net)
                tlsList[trafficlightId.get("id")] = tls
            logging.info('Pre initializing process finished!')
        except Exception:
            logging.error("Error while initializing TLS")
            logging.exception("Error-Message: ")
        return tlsList

    def __initTlsTimestamps(self):

        tlTimestamps = {}
        for tls in self.TLS:
            tlTimestamps[tls._id] = 90
        return tlTimestamps

    def setTlsPhases(self, phases):
        self.tlsPhases = phases

    def split_list(self, a_list):
        half = len(a_list) // 2
        return a_list[:half], a_list[half:]

    def setVehiclesPerTls(self):
        # this function iterates over every active vehicle inside the SUMO Simulation
        # every vehicle gets assigned to its next tls

        idl = traci.vehicle.getIDList()
        try:
            self.vehiclesPerTls = copy.deepcopy(self.vehiclesPerTlsModel)
            self.nextVehiclesPerTls = copy.deepcopy(self.nextVehiclesPerTlsModel)
            for i in range(len(idl)):
                vehIDTmp = idl[i]
                tlsVehData = traci.vehicle.getNextTLS(vehIDTmp)
                if len(tlsVehData) > 0:
                    if len(tlsVehData) == 1:
                        tlsVehDict = {"distance": tlsVehData[0][2], "nextTls": None, "nextTlsDistance": None}
                    else:
                        tlsVehDict = {"distance": tlsVehData[0][2], "nextTls": tlsVehData[1][0], "nextTlsDistance": tlsVehData[1][2]}
                        tmpNext = self.nextVehiclesPerTls[tlsVehData[1][0]]
                        tmpNext[vehIDTmp] = {"nextTls": tlsVehData[1][0], "nextTlsDistance": tlsVehData[1][2]}
                    tmp = self.vehiclesPerTls[tlsVehData[0][0]]
                    tmp[vehIDTmp] = tlsVehDict
        except Exception as e:
            logging.error("Error while compute vehicles per TLS")
            logging.exception("Error-Message: ", e)

    def initNextStep(self):
        # every instance of the TrafficLightSystem class will be updated with the actual step information
        # moreover the anonymity and count per phase duration calculations are triggered at the end of each
        # function call

        tls = self.tls.get(self.tlsId)
        try:
            if self.step == 2:
                tls.getNode()

            if self.step != 0:
                decision = self.tlsInformationsClass.getTlsDecision(self.tlsId)
            else:
                decision = self.defaultDecisions.get(self.tlsId)

            if self.tlsId in self.vehiclesPerTls.keys():
                incVehicles = self.vehiclesPerTls[self.tlsId]
                nextIncVehicles = self.nextVehiclesPerTls[self.tlsId]
            else:
                incVehicles = {}
                nextIncVehicles = {}

            if simInfo.GENERATE_STATISTICS:
                if self.step == tls.secondYellowPhase:
                    self.statisticsHandler.getAmountPerQuasiIdentifier(self.tlsId, tls, self.step, self.tlsInformationsClass.getArrivalDistance(self.tlsId))
                self.statisticsHandler.getVehiclesPerPhaseDuration(self.tlsId, incVehicles, self.statisticsHandler.getPrevIncVehicles(self.tlsId), self.step, tls.getSecondYellowPhase())
                tls.nextStep(decision, self.step, incVehicles, nextIncVehicles, self.tlsPhases)
                self.statisticsHandler.setPrevIncVehicles(self.tlsId, incVehicles)
            else:
                tls.nextStep(decision, self.step, incVehicles, nextIncVehicles, self.tlsPhases)
        except Exception as e:
            logging.error("Error while inititalizing next step for TLS : %s", str(self.tlsId))
            logging.exception("Error-Message: ", e)

        return tls

    def setTlsId(self, tlsId):
        self.tlsId = tlsId

    def setStep(self, step):
        self.step = step

    def getTls(self, tlsid):
        return self.tls.get(tlsid)

    def getNextVehiclesPerTls(self):
        return self.nextVehiclesPerTls
