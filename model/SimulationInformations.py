# this file is used to declare env variables that are used from multiple modules
# with this way circular import error is avoided

LOGGING_FILENAME = "simlogging"
SUMMARY_FILENAME = "summary"
TRIPINFO_FILENAME = "tripinfo"
STATISTICS_FILENAME = "statistics"
ANONYMITY_FILENAME = "anonymity"
OUTPUT_DIR = "output"

# the simulation type defines which kind of simulation shall be started
# TYPES: simulation, defaultSimulation
SIMULATION_TYPE = "defaultSimulation"

# this variable controls the anonymity clustering mechanism
# when this is active the privacy level will raise while the performance will drop a little bit
ANONYMITY_CLUSTERING = False

# when this is set to true arrivalDistance and phaseDuration will be modified based on traffic amount -> InVehSt
# if set to False the standard iTLM-Q Framework with no information exchange between TLS is used
IN_VEH_ST = False

# when activated the simulation generates statistics.xml and anonymity.xml as output files
# only relevant when type simulation is used
GENERATE_STATISTICS = False

# defines if the simulation shall be run with a GUI or not
# when running on a server, GUI needs to be disabled
GUI = True

# this variables scales the amount of traffic occuring during the simulation
SCALE = 1

# this list defines which TLS should be controlled via the iTLM-Q Algorithm
# for every TLS to be controlled, the id and the phase length information is needed
TRAFFIC_LIGHT_IDS = [{"id": "cluster_21532613_25633348", "phase": 19},
   {"id": "cluster_25579770_2633530003_2633530004_2633530005", "phase": 18},
   {"id": "gneJ207", "phase": 8},
   {"id": "gneJ210", "phase": 14},
   {"id": "cluster_494830315_cluster_283155103_285141680_3300414849_3300414850_3300414851_792810590_792810596_792810637", "phase": 19},
   {"id": "gneJ143", "phase": 12},
   {"id":"cluster_32564118_371775504", "phase": 8},
   {"id":"gneJ205", "phase": 14},
   {"id": "30965809", "phase": 11},
   {"id": "30965800", "phase": 18},
   {"id": "214620430", "phase": 16},
   {"id": "cluster_1443568606_1834131515_1834131519_1834131548_1834131550", "phase": 19},
   {"id": "cluster_277739062_39732718_89129091_89129092", "phase": 7},
   {"id": "cluster_306484187_cluster_1200363791_1200363826_1200363834_1200363898_1200363927_1200363938_1200363947_1200364074_1200364103_1507566554_1507566556_255882157_306484190", "phase": 12},
   {"id": "gneJ214", "phase": 13}]

"""{"id": "cluster_21532613_25633348", "phase": 19},
   {"id": "cluster_25579770_2633530003_2633530004_2633530005", "phase": 18},
   {"id": "gneJ207", "phase": 8},
   {"id": "gneJ210", "phase": 14},
   {"id": "cluster_494830315_cluster_283155103_285141680_3300414849_3300414850_3300414851_792810590_792810596_792810637", "phase": 19},
   {"id": "gneJ143", "phase": 12},
   {"id":"cluster_32564118_371775504", "phase": 8},
   {"id":"gneJ205", "phase": 14},
   {"id": "30965809", "phase": 11},
   {"id": "30965800", "phase": 18},
   {"id": "214620430", "phase": 16},
   {"id": "cluster_1443568606_1834131515_1834131519_1834131548_1834131550", "phase": 19},
   {"id": "cluster_277739062_39732718_89129091_89129092", "phase": 7},
   {"id": "cluster_306484187_cluster_1200363791_1200363826_1200363834_1200363898_1200363927_1200363938_1200363947_1200364074_1200364103_1507566554_1507566556_255882157_306484190", "phase": 12},
   {"id": "gneJ214", "phase": 13}
"""

# this env variables are regarding the algorithm itself
AIM_VEHICLES_PER_SECOND = 5 / 3

# this var defines the distance at which the tls is recognizing the incoming vehicles
# Notice: this is different from the arrivalDistance var inside the iTLM_Q_Algorithmus.py file , which determines at
# which distance the tls is including vehicles into the computation process to find the best next tls phase
TLS_SENSOR_RANGE = 500  # 500

# this list is used to define for which TLS k-anonymity statistics should be generated
TLSIDS_STATISTICS = ["cluster_277739062_39732718_89129091_89129092",
                     "cluster_306484187_cluster_1200363791_1200363826_1200363834_1200363898_1200363927_1200363938_1200363947_1200364074_1200364103_1507566554_1507566556_255882157_306484190",
                     "gneJ214"]


