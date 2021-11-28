from data_structures import *


# Devices: cost, buildings_amount, id
dev_3 = Device(647.00, 3, 1)
dev_10 = Device(2002.00, 10, 2)
dev_25 = Device(4726.00, 25, 3)
dev_60 = Device(10182.00, 30, 4)


# Optical-fibres: cost (1m), fibers_amount, fiber_type, identifier
of_universal_1 = OpticalFibre(1.79, 2, FiberType.UNIVERSAL, 1)

of_overhead_1 = OpticalFibre(1.91, 4, FiberType.OVERHEAD, 2)
of_overhead_2 = OpticalFibre(3.12, 8, FiberType.OVERHEAD, 3)
of_overhead_3 = OpticalFibre(4.07, 12, FiberType.OVERHEAD, 4)
of_overhead_4 = OpticalFibre(6.35, 24, FiberType.OVERHEAD, 5)

of_sewerage_1 = OpticalFibre(1.75, 4, FiberType.SEWERAGE, 6)
of_sewerage_2 = OpticalFibre(2.89, 8, FiberType.SEWERAGE, 7)
of_sewerage_3 = OpticalFibre(3.75, 12, FiberType.SEWERAGE, 8)
of_sewerage_4 = OpticalFibre(6.03, 24, FiberType.SEWERAGE, 9)


# Nodes: vertical_coordinate, horizontal_coordinate, identifier, node_type
building_1 = Node(50.165220600828455, 19.62491124611842, 370, NodeType.BUILDING)
building_2 = Node(50.16541841465633, 19.624798269662936, 321, NodeType.BUILDING)
building_3 = Node(50.165394291417144, 19.624421675879518, 328, NodeType.BUILDING)
building_4 = Node(50.16513737496914, 19.623954700642553, 125, NodeType.BUILDING)
building_5 = Node(50.164504489359096, 19.62402706082411, 178, NodeType.BUILDING)
building_6 = Node(50.16391978622346, 19.623729853352007, 7, NodeType.BUILDING)
building_7 = Node(50.16471941102935, 19.626010349522282, 338, NodeType.BUILDING)
building_8 = Node(50.165590091558265, 19.623832295091475, 31, NodeType.BUILDING)
building_9 = Node(50.165804789890124, 19.623404862467943, 373, NodeType.BUILDING)
building_10 = Node(50.16531508409728, 19.623310714529236, 274, NodeType.BUILDING)
building_11 = Node(50.16472885965653, 19.62362139355752, 9, NodeType.BUILDING)
building_12 = Node(50.16466734404612, 19.623414267284325, 18, NodeType.BUILDING)
building_13 = Node(50.16441379067168, 19.622913822963586, 333, NodeType.BUILDING)
building_14 = Node(50.1654264989326, 19.622813073078344, 298, NodeType.BUILDING)
building_15 = Node(50.1652804882363, 19.622506535771933, 280, NodeType.BUILDING)
building_16 = Node(50.165834789311226, 19.62280911167963, 179, NodeType.BUILDING)
building_17 = Node(50.16580855752822, 19.622155916494386, 13, NodeType.BUILDING)
building_18 = Node(50.16581962561616, 19.621677519978743, 225, NodeType.BUILDING)
building_19 = Node(50.166044093118266, 19.62329692984834, 11, NodeType.BUILDING)
building_20 = Node(50.166098914033064, 19.62368206216528, 22, NodeType.BUILDING)
building_21 = Node(50.16638589712646, 19.62417360284158, 190, NodeType.BUILDING)
building_22 = Node(50.16712102422911, 19.623630678006876, 212, NodeType.BUILDING)
building_23 = Node(50.16715445802267, 19.62311586810893, 35, NodeType.BUILDING)
building_24 = Node(50.166814059717545, 19.622522772262208, 339, NodeType.BUILDING)
building_25 = Node(50.166483330386235, 19.621646232634316, 12, NodeType.BUILDING)
list_b = [building_1,building_2,building_3,building_4,building_5,
            building_6,building_7,building_8,building_9,building_10,
            building_11,building_12,building_13,building_14,building_15,
            building_16,building_17,building_18,building_19,building_20,
            building_21,building_22,building_23,building_24,building_25]

pole_1 = Node(50.16523082647023, 19.625340629501924,9001,NodeType.POLE)
pole_2 = Node(50.16539971054326, 19.625022100248128,9002,NodeType.POLE)
pole_3 = Node(50.16566418770367, 19.624639911057525,9003,NodeType.POLE)
pole_4 = Node(50.16598341979715, 19.624458746982672,9004,NodeType.POLE)
pole_5 = Node(50.166313225614346, 19.62429723056375,9005,NodeType.POLE)
pole_6 = Node(50.166788456864744, 19.623995875240766,9006,NodeType.POLE)
pole_7 = Node(50.1660412028144, 19.623921019289572,9007,NodeType.POLE)
pole_8 = Node(50.165959589586954, 19.623551671546338,9008,NodeType.POLE)
pole_9 = Node(50.16589181651715, 19.623155051980078,9009,NodeType.POLE)
pole_10 = Node(50.16599977628438, 19.622817895014755,9010,NodeType.POLE)
pole_11 = Node(50.16547507510575, 19.624193874790684,9011,NodeType.POLE)
pole_12 = Node(50.165281055413196, 19.62389039997394,9012,NodeType.POLE)
pole_13 = Node(50.165107809337634, 19.62349144006858,9013,NodeType.POLE)
pole_14 = Node(50.164818965739734, 19.623433411706582,9014,NodeType.POLE)
list_p = [pole_1,pole_2,pole_3,pole_4,pole_5,pole_6,pole_7,pole_8,pole_9,pole_10,pole_11,pole_12,pole_13,pole_14]

# Just for test calculate_distance
# e_1 = Edge(pole_1,pole_14,FiberType.SEWERAGE,of_universal_1,1)
# print(e_1.distance)

def add_poles_to_network(network: Network):
    pass

def add_buildings_to_network(network: Network):
    pass

def add_devices_to_network(network: Network):
    pass

def add_edges_to_network(network: Network):
    pass
