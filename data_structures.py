import builtins
from enum import Enum
from typing import List
from numpy import inf,sin,arcsin,sqrt,deg2rad  
import gmplot
import copy

class NodeType(Enum):
    BUILDING = 0
    POLE = 1
    START_POINT = 2

class FiberType(Enum):
    UNIVERSAL = 0
    OVERHEAD = 1
    SEWERAGE = 2

# Cost by 1m of different type of assembly
assembly_cost_1m = {
    None : 0,
    FiberType.UNIVERSAL : 10,
    FiberType.OVERHEAD : 10,
    FiberType.SEWERAGE : 50
}


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


# Node can be a building or pole
class Node:
    def __init__(self, vertical_coordinate: float, horizontal_coordinate: float, identifier: int, node_type: NodeType) -> None:
        self.vert_coord = vertical_coordinate       # E.g. 50.1652214 [N]
        self.hori_coord = horizontal_coordinate     # E.g. 19.6248754 [E]
        self.id = identifier                        # Number, buildings and poles can't have the same id, e.g. 370
        self.type = node_type                       # Type of node, enum NodeType (building or pole), e.g. NodeType.
        self.devices = []                           # Devices, [class Device, ...]

    def add_device(self, device: Device) -> None:
        self.devices.append(device)
        
    def remove_device(self, identifier):
        for idx, device in enumerate(self.devices):
            if device.idx == identifier:
                del self.devices[idx]
                break

    def measure_distance(self, node) -> float:
        lat_1, lon_1 = self.vert_coord, self.hori_coord 
        lat_2, lon_2 = node.vert_coord, node.hori_coord
        r = 6371000                                 # Earth radius
        distance = 2*r*arcsin(sqrt((sin(deg2rad((lat_2 - lat_1)/2)))**2 +(1-(sin(deg2rad((lat_2 - lat_1)/2))**2)\
                    -(sin(deg2rad((lat_2 + lat_1)/2)))**2)*(sin(deg2rad((lon_2 - lon_1)/2)))**2))
        return distance                             # Return distance in [m]


class Edge:  
    def __init__(self, node_start: Node, node_end: Node) -> None:  # other_nodes: Node
        self.start = node_start                         # The begining of the edge, class Node (always type = NodeType.BUILDING)
        self.end = node_end                             # The end of the edge, class Node (always type = NodeType.BUILDING)
        #self.other = other_nodes                       # Other nodes in this edge, e.g. NodeType.POLE
        self.optical_fibres = []                        # List of optical fibre, [class OpticalFibre, ...]
        self.type = None                                # Type of the edge, e.g. FiberType.SEWERAGE
        self.idx = None                                 # Number, edges can't have the same idx in one network, e.g. 4
        self.max_capacity = 0                           # Number, maximal capacity
        self.actual_capacity = 0                        # Number, actual capacity
        self.distance = self.calculate_distance()       # Distance in [m], e.g. 42.42
        self.price = self.calculate_price()             # Price in [zl], e.g. 684.78

    def calculate_distance(self) -> float:
        lat_1, lon_1 = self.start.vert_coord, self.start.hori_coord 
        lat_2, lon_2 = self.end.vert_coord, self.end.hori_coord
        r = 6371000                                 # Earth radius
        distance = 2*r*arcsin(sqrt((sin(deg2rad((lat_2 - lat_1)/2)))**2 +(1-(sin(deg2rad((lat_2 - lat_1)/2))**2)\
                    -(sin(deg2rad((lat_2 + lat_1)/2)))**2)*(sin(deg2rad((lon_2 - lon_1)/2)))**2))
        return distance                             # Return distance in [m]
        
    def calculate_price(self) -> float:  
        assembly_cost = self.distance * assembly_cost_1m[self.type]
        optical_fiber_cost = 0
        for opt_fib in self.optical_fibres:
            optical_fiber_cost += self.distance * opt_fib.price
        return assembly_cost + optical_fiber_cost    # Return price in [zl]

    def calculate_actual_capacity(self) -> int:
        max_capacity = 0 
        for optical_fibre in self.optical_fibres:
            max_capacity += optical_fibre.fib_amount
        return max_capacity

    def add_optical_fibre(self, optical_fibre_type: OpticalFibre):
        self.optical_fibres.append(optical_fibre_type)

        if self.type == None:                        # Add type of edge
            self.type = optical_fibre_type.type

        if self.type != optical_fibre_type.type:     # Check optical fibre type
            print("Error: Two different types of optical fibre in one edge !!!")

        self.price = self.calculate_price()                 # Update edge price
        self.max_capacity = self.calculate_actual_capacity()  # Update max edge capacity

    def remove_optical_fibre(self, identifier: int):
        for idx, optical_fibre in enumerate(self.optical_fibres):
            if optical_fibre.id == identifier:
                del self.optical_fibres[idx]
                self.max_capacity = self.calculate_actual_capacity()
                break
        
        if len(self.optical_fibres) == 0:           # Update type if edge haven't the optical fibre inside
            self.type = None

        self.price = self.calculate_price()                 # Update edge price
        self.max_capacity = self.calculate_actual_capacity  # Update max edge capacity

    def clear(self):
        self.optical_fibres.clear()
        self.price = self.calculate_price()                   # Update edge price
        self.max_capacity = self.calculate_actual_capacity()  # Update max edge capacity

class OpticalFibreNetwork:
    def __init__(self) -> None:
        self.buildings = []     # Buildings in network
        self.poles = []         # Poles in network

        self.edges = dict()     # Edges in graph, adjacency list (dictionary of list)
        self.edges_idxs = []    # Indexes of edges
        
        self.devices = dict()   # Devices in network 
        self.devices_idxs = []  # Indexes of devices

        self.all_nodes = []     # Poles and buildings in network

        self.cost = 0         # Cost of the network
        self.INSTALATION_COST = 250  # [zl]
        self.START_POINT = None

    def add_starting_point(self, vert_coord: float, hori_coord: float, id = 0) -> None:
        self.START_POINT = Node(vert_coord, hori_coord, id, NodeType.START_POINT)
        self.all_nodes.append(self.START_POINT)

    def add_building(self, vert_coord: float, hori_coord: float, id: int) -> None:
        building = Node(vert_coord, hori_coord, id, NodeType.BUILDING)
        self.buildings.append(building)
        self.all_nodes.append(building)

    def add_buildings_from_txt(self, filename: str) -> None:
        with open(filename, 'r') as f:
            for line in f.readlines():
                line.strip()
                v_c, h_c, id = line.split(" ", 2)
                self.add_building(float(v_c), float(h_c), int(id))
    
    def save_buildings_to_txt(self, filename = None) -> None:
        with open(filename, "w") as f:
            for building in self.buildings:
                f.write(str(building.vert_coord)+' '+str(building.hori_coord)+' '+str(building.id))
                f.write('\n')

    def remove_building(self, id: int) -> None:
        for idx, building in enumerate(self.buildings):
            if building.id == id:
                del self.buildings[idx]
                break
    
    def add_pole(self, vert_coord: float, hori_coord: float, id: int) -> None:
        pole = Node(vert_coord, hori_coord, id, NodeType.POLE)
        self.poles.append(pole)
        self.all_nodes.append(pole)

    def add_poles_from_txt(self, filename: str) -> None:
        with open(filename, 'r') as f:
            for line in f.readlines():
                line.strip()
                v_c, h_c, id = line.split(" ", 2)
                self.add_pole(float(v_c), float(h_c), int(id))

    def save_poles_to_txt(self, filename: str) -> None:
        with open(filename, "w") as f:
            for pole in self.poles:
                f.write(str(pole.vert_coord)+' '+str(pole.hori_coord)+' '+str(pole.id))
                f.write('\n')

    def remove_pole(self, id: int) -> None:
        for idx, pole in enumerate(self.poles):
            if pole.id == id:
                del self.poles[idx]
                break
    
    def add_device(self, device: Device, node: Node) -> None:  # TODO: New implementation (adjacency list needed)
        self.devices_idxs.sort()
        new_dev = copy.copy(device)
        idx = 1
        for dev_idx in self.devices_idxs:
            if dev_idx == idx:
                idx += 1
            else:
                break
        new_dev.idx = idx

        if node in self.devices:
            if type(self.devices[node]) == list:
                if new_dev not in self.devices[node]:
                    self.devices[node].append(new_dev)
        else:
            self.devices[node] = [new_dev]
        
        node.add_device(new_dev)
        self.devices_idxs.append(idx)

    def remove_device(self, idx: int) -> None:  # TODO: New implementation (adjacency list needed)
        for node in list(self.devices):
            for dev in self.devices[node]:
                if dev.idx == idx:
                    self.devices[node].remove(dev)
                    node.remove_device(idx)
                break  
            if len(self.devices[node]) == 0:
                del self.devices[node]
        self.devices_idxs.remove(idx)

    def add_edge(self, node_start: Node, node_end: Node) -> None:
        edge_exist = 0
        if node_start in self.edges:
            for edges in self.edges[node_start]:
                if edges.end.id == node_end.id:
                    edge_exist = 1
                    break

        if node_end in self.edges:
            for edges in self.edges[node_end]:
                if edges.end.id == node_start.id:
                    edge_exist = 1
                    break

        if not edge_exist:
            new_edge = Edge(node_start, node_end)

            self.edges_idxs.sort()
            idx = 1
            for edge_idx in self.edges_idxs:
                if edge_idx == idx:
                    idx += 1
                else:
                    break
            new_edge.idx = idx  
            self.edges_idxs.append(idx)

            if node_start in self.edges:
                if type(self.edges[node_start]) == list:
                    self.edges[node_start].append(new_edge)
            else:
                self.edges[node_start] = [new_edge]

            if node_end in self.edges:
                if type(self.edges[node_end]) == list:
                    self.edges[node_end].append(new_edge)
            else:
                self.edges[node_end] = [new_edge]

    def remove_edge(self, idx: int) -> None:
        for node in list(self.edges):
            for edge in self.edges[node]:
                if edge.idx == idx:
                    self.edges[node].remove(edge)

                break  
            if len(self.edges[node]) == 0:
                del self.edges[node]
        self.edges_idxs.remove(idx)
    
    def dct_to_list(self):
        list_ = []
        for node in self.edges:
            for edge in self.edges[node]:
                if edge not in list_:
                    list_.append(edge)
        return list_

    def calculate_objective_function(self) -> None:
        self.cost = 0  # Reset cost of objective function

        self.cost += len(self.buildings) * self.INSTALATION_COST # Instalation cost fot every building
        idx_ = []
        for node in self.devices:  # Cost of devices
            for device in self.devices[node]:
                self.cost += device.price
            
        for node in self.edges:
            for edge in self.edges[node]:
                if edge.idx not in idx_:
                    self.cost += edge.price
                    idx_.append(edge.idx)

    def get_cost(self) -> int:
        return self.cost

    def generate_edges(self, node_id) -> None:
        node_ver, node_hor = 0, 0
        current_node = None
        for node in self.all_nodes:
            if node.id == node_id:
                current_node = node
                break

        node_ver, node_hor = current_node.vert_coord, current_node.hori_coord
        first_quarter = []
        second_quarter = []
        third_quarter = []
        fourth_quarter = []

        for node in self.all_nodes:
            if node.hori_coord == node_hor and node.vert_coord == node_ver:
                pass
            elif node.hori_coord >= node_hor and node.vert_coord >= node_ver:  # 1st quarter
                first_quarter.append(node)
            elif node.hori_coord < node_hor and node.vert_coord >= node_ver:  # 2nd quarter
                second_quarter.append(node)
            elif node.hori_coord < node_hor and node.vert_coord < node_ver:  # 3rd quarter
                third_quarter.append(node)
            elif node.hori_coord > node_hor and node.vert_coord < node_ver:  # 4th quarter
                fourth_quarter.append(node)
        
        best_node_1st_q = None
        best_node_2nd_q = None
        best_node_3rd_q = None
        best_node_4th_q = None

        best_dist_1st_q = inf
        best_dist_2nd_q = inf
        best_dist_3rd_q = inf
        best_dist_4th_q = inf

        if len(first_quarter) >= 1:  # Generate edge between node_id and node from 1st quarter
            for node in first_quarter:
                dist = current_node.measure_distance(node)
                if dist <= best_dist_1st_q:
                    best_dist_1st_q = dist
                    best_node_1st_q = node
            self.add_edge(current_node, best_node_1st_q)

        if len(second_quarter) >= 1:  # Generate edge between node_id and node from 2nd quarter
            for node in second_quarter:
                dist = current_node.measure_distance(node)
                if dist <= best_dist_2nd_q:
                    best_dist_2nd_q = dist
                    best_node_2nd_q = node
            self.add_edge(current_node, best_node_2nd_q)

        if len(third_quarter) >= 1:  # Generate edge between node_id and node from 3rd quarter
            for node in third_quarter:
                dist = current_node.measure_distance(node)
                if dist <= best_dist_3rd_q:
                    best_dist_3rd_q = dist
                    best_node_3rd_q = node
            self.add_edge(current_node, best_node_3rd_q)

        if len(fourth_quarter) >= 1:  # Generate edge between node_id and node from 4th quarter
            for node in fourth_quarter:
                dist = current_node.measure_distance(node)
                if dist <= best_dist_4th_q:
                    best_dist_4th_q = dist
                    best_node_4th_q = node
            self.add_edge(current_node, best_node_4th_q)

    def visualization(self, show_id = False, show_empty_edge = False) -> None:
        # Create the map plotter:
        apikey = 'AIzaSyBal6A70lGi745Rm8Fdk0o5FZEleeHhBLI' # (your API key here)
        gmap = gmplot.GoogleMapPlotter(50.165997404672005, 19.625832486967628, 17, apikey=apikey)

        # Highlight buildings:
        if len(self.buildings) != 0:
            buildings_ = [0 for i in range(len(self.buildings))]
            for i in range(len(self.buildings)):
                buildings_[i] = (self.buildings[i].vert_coord, self.buildings[i].hori_coord)
                if show_id == True:
                    gmap.text(self.buildings[i].vert_coord, self.buildings[i].hori_coord, str(self.buildings[i].id))
            building_y, building_x = zip(*buildings_)
            gmap.scatter(building_y, building_x, color='orangered', size=4, marker=False,alpha = 1)
        # Highlight poles:
        if len(self.poles) != 0:
            poles_ = [0 for i in range(len(self.poles))]
            for i in range(len(self.poles)):
                poles_[i] = (self.poles[i].vert_coord,self.poles[i].hori_coord)
                if show_id == True:
                    gmap.text(self.poles[i].vert_coord, self.poles[i].hori_coord, str(self.poles[i].id))
            poles_y, poles_x = zip(*poles_)
            gmap.scatter(poles_y, poles_x, color='k', size=2, marker=False, symbol = 'x')

        # Create connection between two nodes
        if len(self.edges) != 0:
            edges_ = self.dct_to_list()
            for i in range(len(edges_)):
                if edges_[i].type == FiberType.OVERHEAD:
                    color = 'royalblue'
                elif edges_[i].type == FiberType.UNIVERSAL:
                    color = 'gold'   
                elif edges_[i].type == FiberType.SEWERAGE:
                    color = 'green'
                else:
                    color = 'gray'
                if edges_[i].type != None:
                    edge_ = zip(*[(edges_[i].start.vert_coord, edges_[i].start.hori_coord),
                            (edges_[i].end.vert_coord, edges_[i].end.hori_coord)])
                    gmap.plot(*edge_, edge_width=4, color=color, alpha = 0.6)
                    gmap.text((edges_[i].start.vert_coord + edges_[i].end.vert_coord)/2, (edges_[i].start.hori_coord + edges_[i].end.hori_coord)/2, str(edges_[i].idx),color = 'dimgray')
                elif edges_[i].type == None and show_empty_edge == True:
                    edge_ = zip(*[(edges_[i].start.vert_coord, edges_[i].start.hori_coord),
                            (edges_[i].end.vert_coord, edges_[i].end.hori_coord)])
                    gmap.plot(*edge_, edge_width=4, color=color, alpha = 0.6)
                    gmap.text((edges_[i].start.vert_coord + edges_[i].end.vert_coord)/2, (edges_[i].start.hori_coord + edges_[i].end.hori_coord)/2, str(edges_[i].idx),color = 'dimgray')

        # Create START_POINT
        if show_id == True:
            gmap.text(self.START_POINT.vert_coord, self.START_POINT.hori_coord, str(self.START_POINT.id))
        gmap.scatter([self.START_POINT.vert_coord], [self.START_POINT.hori_coord], color='darkviolet', size=3, marker=False,alpha = 1,symbol = '+')

        # Draw the map to an HTML file:
        gmap.draw('map.html')