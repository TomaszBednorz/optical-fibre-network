import builtins
from enum import Enum

class NodeType(Enum):
    BUILDING = 0
    POLE = 1


class FiberType(Enum):
    UNIVERSAL = 0
    UVERHEAD = 1
    SEWERAGE = 2


class OpticalFibreName(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9
    K = 10


class DeviceName(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4


# Node can be a building or pole
class Node:
    def __init__(self, vertical_coordinate: float, horizontal_coordinate: float, identifier: int, node_type: NodeType) -> None:
        self.vert_coord = vertical_coordinate       # E.g. 50.1652214 [N]
        self.hori_coord = horizontal_coordinate     # E.g. 19.6248754 [E]
        self.id = identifier                        # Number, buildings and poles can't have the same id, e.g. 370
        self.type = node_type                       # Type of node, enum NodeType (building or pole), e.g. NodeType.


class OpticalFibre:
    def __init__(self, cost: float, fibers_amount: int, fiber_type: FiberType, fiber_name: str) -> None:
        self.price = cost                   # Price in [zl] e.g. 7.44 
        self.fib_amount = fibers_amount     # The amount of fibers, e.g. 8
        self.type = fiber_type              # The type of the optical-fiber, enum FiberType , e.g. FiberType.UVERHEAD
        self.name = fiber_name              # The name of the optical-fiber, OpticalFibreName.A


class Device:
    def __init__(self, cost: float, buildings_amount: int, device_name: OpticalFibreName) -> None:
        self.price = cost                   # Price in [zl] e.g. 325.44 
        self.amount = buildings_amount      # Number of buildings that can be connected to the device, e.g. 16
        self.name = device_name             # The name of the device, e.g. DeviceName.A


class Edge:  
    def __init__(self, node_start: Node, node_end: Node, edge_type: FiberType, optical_fibre_type: OpticalFibre, identifier: int) -> None:  # other_nodes: Node
        self.start = node_start                     # The begining of the edge, class Node (always type = NodeType.BUILDING)
        self.end = node_end                         # The end of the edge, class Node (always type = NodeType.BUILDING)
        #self.other = other_nodes                   # Other nodes in this edge, e.g. NodeType.POLE
        self.type = edge_type                       # Type of the edge, e.g. FiberType.SEWERAGE
        self.optical_fibre = optical_fibre_type     # Type of optical fibre, class OpticalFibre
        self.id = identifier                        # Number, every edge have different id, e.g. 4
        self.distance = self.calculate_distance()   # Distance in [m], e.g. 42.42
        self.price = self.calculate_price()         # Price in [zl], e.g. 684.78

        self.UNIVERSAL_COST_1M = 10                  # Employee cost - for FiberType.UNIVERSAL
        self.UVERHEAD_COST_1M = 10                  # Employee cost - for FiberType.UVERHEAD
        self.SEWERAGE_COST_1M = 30                  # Employee cost - for FiberType.SEWERAGE
        

    def calculate_distance(self) -> float:
        return 0  # TODO: Distance by self.start and self.end
        
    def calculate_price(self) -> float:  # Tu będzie cena za kopanie rowu/wieszanie powietrzem
        return 0  # TODO: Price of edge


class Network:
    def __init__(self) -> None:
        self.buildings = []
        self.poles = []
        self.edges = []  # adjacency list
        self.devices = []
        self.cost = 0

        self.INSTALATION_COST = 50  # [zl]

    def add_building(self, vert_coord: float, hori_coord: float, id: int):  # TODO: this method update the cost (Installation cost)
        self.buildings.append(Node(vert_coord, hori_coord, id, NodeType.BUILDING))

    def remove_building(self, id: int):  # TODO: this method update the cost (Installation cost)
        for idx, building in enumerate(self.buildings):
            if building.id == id:
                del self.buildings[idx]
                break
    
    def add_pole(self, vert_coord: float, hori_coord: float, id: int):
        self.poles.append(Node(vert_coord, hori_coord, id, NodeType.POLE))

    def remove_pole(self, id: int):
        for idx, pole in enumerate(self.poles):
            if pole.id == id:
                del self.poles[idx]
                break
    
    def add_device(self, device: Device):
        


        self.devices.append(device)
            

    def add_edge(): # 2 edges on one time, this method update the cost 
        pass

    def remove_edge(): # 2 edges on one time, this method update the cost 
        pass




