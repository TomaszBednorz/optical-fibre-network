
class Building:
    def __init__(self, ver_coord, hor_coord) -> None:
        self.vertical_coordinate = ver_coord  # e.g. 50.1652214 [N]
        self.horizontal_coordinate = hor_coord  # e.g. 19.6248754 [E]




class Pole:
    def __init__(self) -> None:
        pass


class OpticalFibre:
    def __init__(self) -> None:
        pass


# TODO: distance, type od connection, 
class Edge:  
    def __init__(self) -> None:
        pass


class Network:
    def __init__(self) -> None:
        buildings = []
        poles = []


# TODO: Data structure for final solution / or maybe part of Network class (things like edges with type of connections)
class Graph:
    def __init__(self) -> None:
        self.neightborhood_list = None # to be completed