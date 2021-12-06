from numpy import number
from data_structures import *
import random


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


    def create_beginning_solution(self) -> None:
        self.actual_solution = self.empty_network
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

            if current_edge not in visited_edges:
                visited_edges.append(current_edge)
            
                if current_edge.distance >= self.MAX_OVERHEAD_DISTANCE:  # Add optical fibre to node
                    current_edge.add_optical_fibre(of_sewerage_1)
                else:
                    current_edge.add_optical_fibre(of_overhead_1)
            else:
                if current_edge in visited_edges:
                    if current_edge.type == FiberType.OVERHEAD:
                        current_edge.add_optical_fibre(of_overhead_1)
                    else:
                        current_edge.add_optical_fibre(of_sewerage_1)

            if current_node.id == current_edge.start.id:
                current_node = current_edge.end  # Update current node
            else:
                current_node = current_edge.start 

            node_edges = self.actual_solution.edges[current_node]

            if current_node.type == NodeType.BUILDING:
                if current_node not in visited_buildings:
                    visited_buildings.append(current_node)

            iterator += 1
            if iterator >= 100:  # Add device to node and optical fibre to previous edges every 200 iteration
                self.actual_solution.add_device(dev_4, current_node)
                iterator = 0
                for edge in visited_edges:
                    if edge.type == FiberType.OVERHEAD:
                        edge.add_optical_fibre(of_overhead_1)
                    else:
                        edge.add_optical_fibre(of_sewerage_1)

    def device_neighbourhood(self) -> None:
        pass

    def edge_neighbourhood(self) -> None:
        pass
        
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

        s = network.START_POINT.id
        d = dict()            # Checking optical fibers
        p = dict()

        for node in network.all_nodes:
            d[node.id] = float('inf')
            p[node.id] = None
        
        d[s] = 0

        for i in range(len(network.all_nodes)-1):
            for node in network.all_nodes:
                for edge in network.edges[node]:
                    if edge.type != None:
                        if d[edge.end.id] > d[node.id] + edge.distance:    # chyba moze byc tez edge.start
                            d[edge.end.id] =  d[node.id] + edge.distance
                            p[edge.end.id] = node.id
        
        for node in network.all_nodes:    # Raczej nie będzie cyklu więc będzie można usunąć
            for edge in network.edges[node]:
                if edge.type != None:
                    if d[edge.end.id] <= d[node.id] + edge.distance:   
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