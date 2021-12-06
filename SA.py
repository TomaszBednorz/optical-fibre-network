from numpy import number
from data_structures import *
import random
import copy

# Devices: cost, buildings_amount, id
dev_4 = Device(863.00, 4, 1)
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

class SimulatedAnnealing:
    def __init__(self, network: OpticalFibreNetwork) -> None:
        self.empty_network = network
        self.actual_solution = None
        self.best_solution = None

        self.MAX_OVERHEAD_DISTANCE = 40  # [m]


    def create_beginning_solution(self, num_of_iterations: int) -> None:
        self.actual_solution = copy.deepcopy(self.empty_network)
        for node in self.actual_solution.all_nodes:
            self.actual_solution.generate_edges(node.id)

        visited_edges = []
        visited_buildings = []
        current_node = self.actual_solution.START_POINT
        self.actual_solution.add_device(dev_4, current_node)
        iterator = 0
        node_edges = self.actual_solution.edges[current_node]

        while len(visited_buildings) < len(self.actual_solution.buildings):
            rand_num = random.randint(0, len(node_edges) - 1)
            current_edge = node_edges[rand_num]

            if current_edge not in visited_edges:  # Add optical fibre to node
                visited_edges.append(current_edge)
            
                if current_edge.distance >= self.MAX_OVERHEAD_DISTANCE:
                    current_edge.add_optical_fibre(of_sewerage_1)
                else:
                    current_edge.add_optical_fibre(of_overhead_1)
            else:
                if current_edge in visited_edges:
                    if current_edge.type == FiberType.OVERHEAD:
                        current_edge.add_optical_fibre(of_overhead_1)
                    else:
                        current_edge.add_optical_fibre(of_sewerage_1)

            if current_node.id == current_edge.start.id:  # Update current node
                current_node = current_edge.end
            else:
                current_node = current_edge.start 

            node_edges = self.actual_solution.edges[current_node]

            if current_node.type == NodeType.BUILDING:
                if current_node not in visited_buildings:
                    visited_buildings.append(current_node)

            iterator += 1
            if iterator >= num_of_iterations:  # Add device to node and optical fibre to previous edges every 50 iteration
                self.actual_solution.add_device(dev_4, current_node)
                iterator = 0
                for edge in visited_edges:
                    if edge.type == FiberType.OVERHEAD:
                        edge.add_optical_fibre(of_overhead_1)
                    else:
                        edge.add_optical_fibre(of_sewerage_1)

    def update_device_neighbourhood(self, ) -> None:
        pass

    def update_node_neighbourhood(self, max_num_of_of: int, type_of_node: NodeType) -> OpticalFibreNetwork:
        possible_of_overhead = [of_overhead_1, of_overhead_2, of_overhead_3, of_overhead_4]
        possible_of_sewerage = [of_sewerage_1, of_sewerage_2, of_sewerage_3, of_sewerage_4]

        neighbourhood_solution = copy.deepcopy(self.actual_solution)  # Deep copy of actual solution

        rand_num = 0  # Number to choose node for optimization
        node = None
        
        list_of_optical_fibres = []
        if type_of_node == NodeType.BUILDING:
            rand_num = random.randint(0, len(neighbourhood_solution.buildings) - 1)
            node = neighbourhood_solution.buildings[rand_num]
            rand_of = random.randint(1, max_num_of_of)
        elif type_of_node == NodeType.POLE:
            rand_num = random.randint(0, len(neighbourhood_solution.poles) - 1)
            node = neighbourhood_solution.poles[rand_num]
            rand_of = random.randint(0, max_num_of_of)

        node_edges = neighbourhood_solution.edges[node]
        rand_num_of_edges = random.randint(1, len(node_edges) - 1)
        
        for edge in node_edges:  # Delete all edges of this node and add empty edges
            neighbourhood_solution.remove_edge(edge.idx)  
            neighbourhood_solution.add_edge(edge.start, edge.end)

        used_edges = []
        it_num = 0

        for i in range(rand_num_of_edges):
            rand_edge = random.randint(0, len(node_edges) - 1)
            if node_edges[rand_edge] not in used_edges:
                used_edges.append(node_edges[i])
                for _ in range(rand_of):
                    if node_edges[rand_edge].distance >= self.MAX_OVERHEAD_DISTANCE:
                        type_of_op = possible_of_sewerage[random.randint(0, 3)]
                    else:
                        type_of_op = possible_of_overhead[random.randint(0, 3)]
                    node_edges[rand_edge].add_optical_fibre(type_of_op)
                    
        return neighbourhood_solution
        
        



    def check_network_correctness(self, network: OpticalFibreNetwork) -> bool:
        number_of_buildings = len(network.buildings)                # Chcecking devices
        number_of_devices = 0
        number_of_max_buildings = 0
        for node in network.all_nodes:
            if len(node.devices) != 0:
                for device in node.devices:
                    number_of_devices += 1
                    number_of_max_buildings += device.amount    
        if number_of_max_buildings >= number_of_buildings:
            correct = True
        else: 
            correct =  False
        print("Number of devices: {} , number of buildings that can be connected to the device: {} .".format(number_of_devices,number_of_max_buildings))
        print("Number of buildings: {} .".format(number_of_buildings))

        if correct == False:
            return correct

        s = network.START_POINT.id                                  # Checking optical fibers, Bellman-Ford algorithm
        d = dict()            
        p = dict()

        for node in network.all_nodes:
            d[node.id] = float('inf')
            p[node.id] = None
        
        d[s] = 0

        for i in range(len(network.all_nodes)-1):
            for node in network.all_nodes:
                for edge in network.edges[node]:
                    if edge.type != None:
                        if node.id == edge.start.id:
                            if d[edge.end.id] > d[node.id] + edge.distance:   
                                d[edge.end.id] =  d[node.id] + edge.distance
                                p[edge.end.id] = node.id
                        elif node.id == edge.end.id:
                            if d[edge.start.id] > d[node.id] + edge.distance:    
                                d[edge.start.id] =  d[node.id] + edge.distance
                                p[edge.start.id] = node.id
        
        for node in network.all_nodes:   
            for edge in network.edges[node]:
                if edge.type != None:
                    if node.id == edge.start.id:
                        if d[edge.end.id] <= d[node.id] + edge.distance:   
                            continue
                        else:
                            print("Cykl ujemny!")
                    elif node.id == edge.end.id:
                        if d[edge.start.id] <= d[node.id] + edge.distance:   
                            continue
                        else:
                            print("Cykl ujemny!")

        edges_ = {}
        list_edges = network.dct_to_list()
        for building in network.buildings:
            current = building.id
            while current:
                for edge_ in list_edges:
                    if (edge_.start.id == current and edge_.end.id == p[current]) or (edge_.end.id == current and edge_.start.id == p[current]):
                        if edge_.idx in edges_:
                            edges_[edge_.idx] += 1
                        else:
                            edges_[edge_.idx] = 1
                current = p[current]
        print(edges_)
        for ed in edges_:
            for ed_ in list_edges:
                if ed == ed_.idx:
                    print(edges_[ed],ed_.max_capacity)
                    max = ed_.max_capacity
                    break
            if edges_[ed] <= max:
                correct = True
            else:
                return False
        return True

    def run_alghoritm(self) -> None:
        pass