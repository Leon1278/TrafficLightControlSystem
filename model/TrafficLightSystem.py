import traci
import logging
import model.SimulationInformations as simInfo

logging.basicConfig(filename=f'{simInfo.OUTPUT_DIR}/{simInfo.LOGGING_FILENAME}.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')


# this class represents a TrafficLightSystem
class TrafficLightSystem:

    def __init__(self, tls, net):
        self.step = None
        self.incVehicles = None
        self.nextIncVehicles = None
        self.decision = None
        self.phases = None
        self.incEdges = None
        self.outEdges = None
        self.incEdgesStripped = None
        self.nextEdges = None
        self.incSplit = None
        self.actualEdges = None
        self.net = net
        self.id = tls._id
        self.phase = traci.trafficlight.getRedYellowGreenState(self.id)
        self.lanes = self.__getLanes()
        self.tls = tls
        self.connections = self.tls._connections
        self.edges = self.__getEdges()
        self.programs = traci.trafficlight.getAllProgramLogics(self.id)
        self.node = self.getNode()
        self.phaseDuration = 30
        self.secondYellowPhase = 0
        self.firstYellowPhase = 6
        self.greenPhase = 12

    def nextStep(self, decision, step, incVehicles, nextIncVehicles, phases):
        # this function gets called from the tls initializer instance and is used to keep the
        # tls attributes updated each simulation step

        self.decision = decision
        self.phase = traci.trafficlight.getRedYellowGreenState(self.id)
        self.step = step
        self.incVehicles = incVehicles
        self.nextIncVehicles = nextIncVehicles
        self.phases = phases
        self.incSplit = self.initIncSplit()
        self.actualEdges, self.nextEdges = self.__getActualAndNextEdges()

    def getNode(self):
        # a Node represents a junction when using sumolib, in most cases the trafficLightId is identical
        # to the node id but not in ever case. For this reason there is a if construct to assign the correct
        # tls and node id
        try:
            if self.id == "gneJ214":
                self.node = self.net.getNode("cluster_1723628632_cluster_1723628638_1834131513_1834131518_40091377")
            elif self.id == "gneJ205":
                self.node = self.net.getNode("cluster_3300416901_792810649_cluster_3300416888_3300416892_3300416903_cluster_307632375_3300416891_3300416896_335543933")
            elif self.id == "gneJ210":
                self.node = self.net.getNode("cluster_371462086_469470779_98101387_cluster_371462067_371775459_371775468")
            elif self.id == "gneJ143":
                self.node = self.net.getNode("cluster_1041665625_cluster_1387938793_1387938796_cluster_1757124361_1757124367_32564126")
            elif self.id == "gneJ207":
                self.node = self.net.getNode("cluster_274083968_cluster_1200364014_1200364088")
            else:
                self.node = self.net.getNode(self.id)
            self.incEdges = self.__getIncEdges()
            self.outEdges = self.__getOutEdges()
            self.incEdgesStripped = self.__getIncEdgesStripped()
        except Exception as e:
            print("No Node for key: ", e)

    def __getIncEdges(self):
        incEdgesList = []
        incEdges = self.node._incoming
        for incEdge in incEdges:
            incEdgesList.append(incEdge._id)
        return incEdgesList

    def __getOutEdges(self):
        outEdgesList = []
        outEdges = self.node._outgoing
        for outEdge in outEdges:
            outEdgesList.append(outEdge._id)
        return outEdgesList

    def __getIncEdgesStripped(self):
        incEdgesList = []
        incEdges = self.node._incoming
        for incEdge in incEdges:
            tmp = incEdge._id.split("#")
            incEdgesList.append(tmp[0])
        return incEdgesList

    def __getPhases(self):
        phases = self.programs[0].phases
        transformedPhases = []
        for phase in phases:
            state = phase.state
            chars = [char for char in state]
            phase = []
            for char in chars:
                if not 'y' in state:
                    if char == 'G' or char == 'g':
                        phase.append(1)
                    elif char == 'r':
                        phase.append(0)
                    transformedPhases.append(phase)
        return transformedPhases

    def __getLanes(self):
        laneIds = traci.trafficlight.getControlledLanes(self.id)
        lanes = []
        for laneId in laneIds:
            lane = self.net.getLane(laneId)
            if not lane in lanes:
                lanes.append(lane)
        return lanes

    def __getEdges(self):

        edges = []
        for lane in self.lanes:
            edge = lane._edge
            if not edge in edges:
                edges.append(edge)
        return edges

    def __setPhase(self, index):

        traci.trafficlight.setPhase(self.id, index)

    def initIncSplit(self):

        incSplit = []
        for i in range(len(self.phases[0])):
            incSplit.append(0)
        return incSplit

    def __getActualAndNextEdges(self):
        # this method identifies the actual and next edge, which is the outgoing edge
        # actual and outgoing edge will then be used to calculate the incoming traffic builtArray()

        actualEdges = {}
        nextEdges = {}
        if len(self.incVehicles) > 0:
            for vehicleId in self.incVehicles:
                if self.incVehicles[vehicleId].get("distance") < simInfo.TLS_SENSOR_RANGE:
                    route = traci.vehicle.getRoute(vehicleId)
                    for edge in self.incEdges:
                        if edge in route:
                            tmp = edge.split("#")
                            actualEdges[vehicleId] = tmp[0]
                    for edge in self.outEdges:
                        if edge in route:
                            tmp = edge.split("#")
                            nextEdges[vehicleId] = tmp[0]
        return actualEdges, nextEdges

    def builtArray(self, vehId, Split):
        # method which sorts a vehicle instance into an array by using its actual and next edge
        # this array represents the incoming vehicle positions

        lanes = self.lanes
        counter = 0
        for i in range(len(lanes)):
            lane = lanes[i]
            connections = lane._outgoing
            actualEdgeIdSplitted = connections[0]._from._id.split("#")
            actualEdgeId = actualEdgeIdSplitted[0]
            toEdges = []
            for connection in connections:
                toEdgeIdSplitted = connection._to._id.split("#")
                toEdgeId = toEdgeIdSplitted[0]
                toEdges.append(toEdgeId)
            for edgeid in toEdges:
                if self.actualEdges.get(vehId) == actualEdgeId and self.nextEdges.get(vehId) == edgeid:
                    Split[counter] += 1
                counter += 1

        return Split

    def getPhases(self):
        return self.phases

    def getPrograms(self):
        return self.programs

    def getStep(self):
        return self.step

    def setStep(self, step):
        self.step = step

    def getPhase(self):
        return self.phase

    def getConnections(self):
        return self.connections

    def getEdges(self):
        return self.edges

    def getId(self):
        return self.id

    def getLanes(self):
        return self.lanes

    def getVehicles(self):
        return self.incVehicles

    def getNextEdges(self):
        return self.nextEdges

    def getActualEdges(self):
        return self.actualEdges

    def getIncSplit(self):
        return self.incSplit

    def getSecondYellowPhase(self):
        return self.secondYellowPhase

    def getPhaseDuration(self):
        return self.phaseDuration

    def setPhaseDuration(self, phaseDuraion):
        self.phaseDuration = phaseDuraion
