import builtins
from enum import Enum
from typing import List
from numpy import sin,arcsin,sqrt,deg2rad  

class NodeType(Enum):
    BUILDING = 0
    POLE = 1


class FiberType(Enum):
    UNIVERSAL = 0
    OVERHEAD = 1
    SEWERAGE = 2

# Cost by 1m of different type of assembly
assembly_cost_1m = {
    FiberType.UNIVERSAL : 10,
    FiberType.OVERHEAD : 10,
    FiberType.SEWERAGE : 30
}


# Node can be a building or pole
class Node:
    def __init__(self, vertical_coordinate: float, horizontal_coordinate: float, identifier: int, node_type: NodeType) -> None:
        self.vert_coord = vertical_coordinate       # E.g. 50.1652214 [N]
        self.hori_coord = horizontal_coordinate     # E.g. 19.6248754 [E]
        self.id = identifier                        # Number, buildings and poles can't have the same id, e.g. 370
        self.type = node_type                       # Type of node, enum NodeType (building or pole), e.g. NodeType.


class OpticalFibre:
    def __init__(self, cost: float, fibers_amount: int, fiber_type: FiberType, identifier: int) -> None:
        self.price = cost                   # Price in [zl] e.g. 7.44 
        self.fib_amount = fibers_amount     # The amount of fibers, e.g. 8
        self.type = fiber_type              # The type of the optical-fiber, enum FiberType , e.g. FiberType.UVERHEAD
        self.id = identifier                # Number, e.g. 3


class Device:
    def __init__(self, cost: float, buildings_amount: int, identifier: int) -> None:
        self.price = cost                   # Price in [zl] e.g. 325.44 
        self.amount = buildings_amount      # Number of buildings that can be connected to the device, e.g. 16
        self.id = identifier                # Number, e.g. 2
        self.idx = None                     # Number, devices can't have the same idx in one network, e.g. 3

class Edge:  
    def __init__(self, node_start: Node, node_end: Node, optical_fibre_type: OpticalFibre) -> None:  # other_nodes: Node
        self.start = node_start                     # The begining of the edge, class Node (always type = NodeType.BUILDING)
        self.end = node_end                         # The end of the edge, class Node (always type = NodeType.BUILDING)
        #self.other = other_nodes                   # Other nodes in this edge, e.g. NodeType.POLE
        self.optical_fibre = optical_fibre_type     # Type of optical fibre, class OpticalFibre
        self.type = self.optical_fibre.type         # Type of the edge, e.g. FiberType.SEWERAGE
        self.idx = None                             # Number, edges can't have the same idx in one network, e.g. 4
        self.distance = self.calculate_distance()   # Distance in [m], e.g. 42.42
        self.price = self.calculate_price()         # Price in [zl], e.g. 684.78

    def calculate_distance(self) -> float:
        lat_1, lon_1 = self.start.vert_coord, self.start.hori_coord 
        lat_2, lon_2 = self.end.vert_coord, self.end.hori_coord
        r = 6371000                                 # Earth radius
        distance = 2*r*arcsin(sqrt((sin(deg2rad((lat_2 - lat_1)/2)))**2 +(1-(sin(deg2rad((lat_2 - lat_1)/2))**2)\
                    -(sin(deg2rad((lat_2 + lat_1)/2)))**2)*(sin(deg2rad((lon_2 - lon_1)/2)))**2))
        return distance                             # Return distance in [m]
        
    def calculate_price(self) -> float:  
        assembly_cost = self.distance * assembly_cost_1m[self.type]
        optical_fiber_cost = self.distance * self.optical_fibre.price
        return assembly_cost + optical_fiber_cost    # Return price in [zl]


class OpticalFibreNetwork:
    def __init__(self) -> None:
        self.buildings = []   # Buildings in network
        self.poles = []       # Poles in network
        self.edges = []       # Edges in graph, adjacency list
        self.devices = []     # Devices in network 
        self.cost = 0         # Cost of the network

        self.INSTALATION_COST = 250  # [zl]

    def add_building(self, vert_coord: float, hori_coord: float, id: int):
        self.buildings.append(Node(vert_coord, hori_coord, id, NodeType.BUILDING))

    def add_buildings_from_txt(Self, filename: str):
        pass

    def remove_building(self, id: int):
        for idx, building in enumerate(self.buildings):
            if building.id == id:
                del self.buildings[idx]
                break
    
    def add_pole(self, vert_coord: float, hori_coord: float, id: int):
        self.poles.append(Node(vert_coord, hori_coord, id, NodeType.POLE))

    def add_poles_from_txt(Self, filename: str):
        pass

    def remove_pole(self, id: int):
        for idx, pole in enumerate(self.poles):
            if pole.id == id:
                del self.poles[idx]
                break
    
    def add_device(self, device: Device):
        idx = 1
        for dev in self.devices:
            if dev.idx == idx:
                idx += 1
            else:
                break
        device.idx = idx
        self.devices.append(device)

    def remove_device(self, idx: int):
        for idx, device in enumerate(self.devices):
            if device.idx == id:
                del self.devices[idx]
                break       

    def add_edge(self, node_start: Node, node_end: Node, optical_fibre_type: OpticalFibre):
        new_edge = Edge(node_start, node_end, optical_fibre_type)
        idx = 1
        for edge in self.edges:
            if edge.idx == idx:
                idx += 1
            else:
                break
        new_edge.idx = idx
        self.edges.append(new_edge)

    def remove_edge(self, idx: int):
        for idx, edge in enumerate(self.edges):
            if edge.idx == idx:
                del self.edges[idx]
                break  

    def calculate_objective_function(self):
        self.cost = 0  # Reset cost of objective function

        self.cost += len(self.buildings) * self.INSTALATION_COST # Instalation cost fot every building

        for device in self.devices:  # Cost of devices
            self.cost += device.price
            
        for edge in self.edges:  # Cost of edges
            self.cost += edge.price

    def get_cost(self):
        return self.cost

    def check_network_correctness(self):  # Devices, fibres (2 for 1 building), etc.
        return False
