import builtins
from enum import Enum

class NodeType(Enum):
    BUILDING = 0
    POLE = 1


class FiberType(Enum):
    UNIVERSAL = 0
    UVERHEAD = 1
    SEWERAGE = 2

# dodac gdziec ceny kopania rowu, usuług zapłaty za montaż itp


# Node can be a building or pole
class Node:
    def __init__(self, vertical_coordinate: float, horizontal_coordinate: float, identifier: int, node_type: NodeType) -> None:
        self.vert_coord = vertical_coordinate       # E.g. 50.1652214 [N]
        self.hori_coord = horizontal_coordinate     # E.g. 19.6248754 [E]
        self.id = identifier                        # Number, buildings and poles can't have the same id, e.g. 370
        self.type = node_type                       # Type of node, enum NodeType (building or pole), e.g. NodeType.
        # Tu to urządzenie jeszcze, pododawać metody(raczej w networku)


class OpticalFibre:
    def __init__(self, cost: float, fibers_amount: int, fiber_type: FiberType, fiber_name: str) -> None:
        self.price = cost                   # Price in [zl] e.g. 7.44 
        self.fib_amount = fibers_amount     # The amount of fibers, e.g. 8
        self.type = fiber_type              # The type of the optical-fiber, enum FiberType , e.g. FiberType.UVERHEAD
        self.name = fiber_name              # The name of the optical-fiber, e.g. '2x9/125 G652D'


class Edge:  
    def __init__(self, node_start: Node, node_end: Node, edge_type: FiberType, identifier: int) -> None:  # other_nodes: Node
        
        self.start = node_start         # The begining of the edge, class Node (always type = NodeType.BUILDING)
        self.end = node_end             # The end of the edge, class Node (always type = NodeType.BUILDING)
        #self.other = other_nodes       # Other nodes in this edge, e.g. NodeType.POLE
        self.type = edge_type           # Type of the edge, e.g. FiberType.SEWERAGE
        self.id = identifier            # Number, every edge have different id, e.g. 4
        self.distance = self.calculate_distance()   # Distance in [m], e.g. 42.42
    
    def calculate_distance() -> float:
        return 0  # TODO: Distance by self.start and self.end
        

class Network:
    def __init__(self) -> None:
        self.buildings = []
        self.poles = []
        self.edges = []  # adjacency list

    def add_building(self, vert_coord: float, hori_coord: float, id: int):
        self.buildings.append(Node(vert_coord, hori_coord, id, NodeType.BUILDING))

    def remove_building(self, id: int):
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
    
    def add_edge():
        pass

    def remove_edge():
        pass


