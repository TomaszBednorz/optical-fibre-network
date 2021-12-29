from numpy import number
from data_structures import *
import random
import copy
import numpy as np
import math

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

class SA_parameters:
    def __init__(self) -> None:
        self.buildings = True
        self.poles = True
        self.devices = True
        self.max_temperature = 100
        self.max_iterations = 100
        self.max_subiterations = 10
        self.alpha = 100

class SimulatedAnnealing:
    def __init__(self, network: OpticalFibreNetwork, param: SA_parameters) -> None:
        self.empty_network = network

        self.begining_solution = None
        self.actual_solution = None
        self.best_solution = None
        self.temporary_solution = None

        self.parameters = param

        self.objective_function_history = []
        self.realizations = [0, 0, 0] # [buildings updates, poles updates, devices updates]
        self.quality_changes = [0, 0, 0] # [worse objective function cost (not accepted), worse objective function cost (accepted), better objective function cost]
        self.quality_changes_it = {
            'worse_not_acepted' : [],
            'worse_accepted': [],
            'better' : []
        }
        self.MAX_OVERHEAD_DISTANCE = 40  # [m]




    def create_beginning_solution(self) -> None:
        self.actual_solution = copy.deepcopy(self.empty_network)
        for node in self.actual_solution.all_nodes:
            self.actual_solution.generate_edges(node.id)

        visited_edges = []
        visited_buildings = []
        current_node = self.actual_solution.START_POINT
        self.actual_solution.add_device(dev_4, current_node)
        iterator = 0
        node_edges = self.actual_solution.edges[current_node]

        if(len(self.actual_solution.buildings)) <= 10:
            num_of_iterations = 25
        elif(len(self.actual_solution.buildings)) <= 20:
            num_of_iterations = 50
        elif(len(self.actual_solution.buildings)) <= 30:
            num_of_iterations = 100
        elif(len(self.actual_solution.buildings)) <= 50:
            num_of_iterations = 200


        while len(visited_buildings) < len(self.actual_solution.buildings):
            rand_num = random.randint(0, len(node_edges) - 1)
            current_edge = node_edges[rand_num]

            if current_edge not in visited_edges:  # Add optical fibre to node
                visited_edges.append(current_edge)
            
                if current_edge.distance >= self.MAX_OVERHEAD_DISTANCE:
                    for _ in range(0, math.ceil(len(self.actual_solution.buildings) / 20)):
                        current_edge.add_optical_fibre(of_sewerage_4)
                else:
                    for _ in range(0, math.ceil(len(self.actual_solution.buildings) / 20)):
                        current_edge.add_optical_fibre(of_overhead_4)

            if current_node.id == current_edge.start.id:  # Update current node
                current_node = current_edge.end
            else:
                current_node = current_edge.start 

            node_edges = self.actual_solution.edges[current_node]

            if current_node.type == NodeType.BUILDING:
                if current_node not in visited_buildings:
                    visited_buildings.append(current_node)

            iterator += 1

            if iterator >= num_of_iterations:  # Add device to node and optical fibre to previous edges every num_of_iterations
                self.actual_solution.add_device(dev_10, current_node)
                iterator = 0
        self.begining_solution = self.actual_solution

    def update_device_neighbourhood(self) -> None:
        possible_devices = [dev_4, dev_10, dev_25, dev_60]

        neighbourhood_solution = copy.deepcopy(self.actual_solution)  # Deep copy of actual solution
        # ----
        rand_num = random.randint(0, len(neighbourhood_solution.all_nodes) - 1)  # Number to choose node for optimization
        node = neighbourhood_solution.all_nodes[rand_num]

        rand_num_of_devices = random.randint(0, 2)

        for div in node.devices:  # Delete devices from node
            neighbourhood_solution.remove_device(div.idx)

        for _ in range(rand_num_of_devices):
            neighbourhood_solution.add_device(possible_devices[random.randint(0, 3)], node)

        neighbourhood_solution.calculate_objective_function()

        return neighbourhood_solution

    def update_node_neighbourhood(self, type_of_node: NodeType) -> OpticalFibreNetwork:
        possible_of_overhead = [of_overhead_1, of_overhead_2, of_overhead_3, of_overhead_4]  # Possible overhead of
        possible_of_sewerage = [of_sewerage_1, of_sewerage_2, of_sewerage_3, of_sewerage_4]  # Possible sewerage of

        neighbourhood_solution = copy.deepcopy(self.actual_solution)  # Deep copy of actual solution

        rand_num = 0  # Number to choose node for optimization
        node = None
        
        if len(neighbourhood_solution.buildings) < 15:
            max_num_of_of = 1  # Max quantity of of in edge
            poss_of_of = 1   # Max index of possible_of_overhead and possible_of_sewerage lists, here 0 and 1
        elif len(neighbourhood_solution.buildings) < 40:
            max_num_of_of = 2
            poss_of_of = 2
        else:
            max_num_of_of = 3
            poss_of_of = 3


        if type_of_node == NodeType.BUILDING:
            rand_num = random.randint(0, len(neighbourhood_solution.buildings) - 1)  # Random number from 0 to length of building list
            node = neighbourhood_solution.buildings[rand_num]  # Node chosen based on rand_num
        elif type_of_node == NodeType.POLE:
            rand_num = random.randint(0, len(neighbourhood_solution.poles) - 1)  # Random number from 0 to length of poles list
            node = neighbourhood_solution.poles[rand_num]  # Node chosen based on rand_num

        node_edges = neighbourhood_solution.edges[node]  # All edges
        rand_num_of_edges = random.randint(1, len(node_edges) - 1)  # Generate random number of edges in node
        
        for edge in node_edges:  # clear all optical fibres in edges of node
            edge.clear()

        used_edges = []  # Used edges, prevents against two the same edges in one node

        for _ in range(rand_num_of_edges):
            rand_edge = random.randint(0, len(node_edges) - 1)  # Generate random edge
            if node_edges[rand_edge] in used_edges:
                rand_edge = random.randint(0, len(node_edges) - 1)
            if node_edges[rand_edge] not in used_edges:
                used_edges.append(node_edges[rand_edge])
                num_of_of = random.randint(0, max_num_of_of)  # Generate number of optical fibres in edge
                for _ in range(num_of_of):
                    if node_edges[rand_edge].distance >= self.MAX_OVERHEAD_DISTANCE:
                        type_of_op = possible_of_sewerage[random.randint(0, poss_of_of)]
                    else:
                        type_of_op = possible_of_overhead[random.randint(0, poss_of_of)]
                    node_edges[rand_edge].add_optical_fibre(type_of_op)
            neighbourhood_solution.calculate_objective_function()
        return neighbourhood_solution

    def check_devices_correctness(self,network: OpticalFibreNetwork) -> bool:
        number_of_buildings = len(network.buildings)                # Chcecking devices
        number_of_devices = 0
        number_of_max_buildings = 0
        for node in network.all_nodes:
            if len(node.devices) != 0:
                for device in node.devices:
                    number_of_devices += 1
                    number_of_max_buildings += device.amount    
        if number_of_max_buildings >= number_of_buildings:
            return True
        else: 
            return False

    def check_fibers_correctness(self,network: OpticalFibreNetwork) -> bool:
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
        # print(edges_)
        for ed in edges_:
            for ed_ in list_edges:
                if ed == ed_.idx:
                    # print(edges_[ed],ed_.max_capacity)
                    max = ed_.max_capacity
                    break
            if edges_[ed] <= max:
                correct = True
            else:
                return False
        return True

    def check_network_correctness(self, network: OpticalFibreNetwork) -> bool:
        I = self.check_devices_correctness(network)
        if I == False:
            return False
        II = self.check_fibers_correctness(network)
        if II == False:
            return False
        else:
            return True

    def calculate_temperature(self,i) -> float:
        return self.parameters.max_temperature * ((self.parameters.max_iterations - i)/self.parameters.max_iterations)
        # return self.max_temperature /  (1 + self.alpha * i)

    def run_alghoritm(self) -> None:
        self.realizations = [0, 0, 0]
        self.quality_changes = [0, 0, 0]
        sol_corect = False
        while not sol_corect:
            self.create_beginning_solution()
            sol_corect = self.check_network_correctness(self.actual_solution)
        self.actual_solution.visualization2(True,False) 
        iterations = 0
        L = self.parameters.max_subiterations
        T = self.parameters.max_temperature
        
        while iterations < self.parameters.max_iterations:
            local_iterations = 0
            while local_iterations < L:
                if self.parameters.buildings and self.parameters.poles and self.parameters.devices:
                    number = random.randint(1,21)
                elif self.parameters.buildings and self.parameters.poles:
                    number = random.randint(1,10)
                elif self.parameters.buildings and self.parameters.devices:
                    number = random.randint(0,11)
                    if number == 11:
                        number = 21
                elif self.parameters.poles and self.parameters.devices:
                    number = random.randint(11,21)
                elif self.parameters.buildings:
                    number = random.randint(1,10)
                elif self.parameters.poles:
                    number = random.randint(11,10)
                elif self.parameters.devices:
                    number = random.randint(21,21)
                else:
                    print("Error! Choose something to optimalization!")

                if 1 <= number <=10:
                    self.temporary_solution = self.update_node_neighbourhood(NodeType.BUILDING)
                elif 11 <= number <=20:
                    self.temporary_solution = self.update_node_neighbourhood(NodeType.POLE)
                elif number == 21:
                    self.temporary_solution = self.update_device_neighbourhood()

                if self.check_network_correctness(self.temporary_solution):
                    local_iterations += 1
                    self.temporary_solution.calculate_objective_function()
                    self.actual_solution.calculate_objective_function()
                    print("Iteration: {} Objective function cost: {}".format(iterations*10+local_iterations, self.temporary_solution.cost))

                    if 1 <= number <=10:
                        self.realizations[0] += 1
                    elif 11 <= number <=20:
                        self.realizations[1] += 1
                    elif number == 21:
                        self.realizations[2] += 1

                    if self.temporary_solution.cost <= self.actual_solution.cost:
                        self.actual_solution = self.temporary_solution
                        self.best_solution = self.actual_solution
                        self.quality_changes[2] += 1
                        self.quality_changes_it['better'].append(iterations*10+local_iterations)
                    elif np.exp(-(self.temporary_solution.get_cost() - self.actual_solution.get_cost())/ T) > random.random():
                        self.actual_solution = self.temporary_solution
                        self.quality_changes[1] += 1
                        self.quality_changes_it['worse_accepted'].append(iterations*10+local_iterations)
                    else:
                        self.quality_changes[0] += 1
                        self.quality_changes_it['worse_not_acepted'].append(iterations*10+local_iterations)


                    self.objective_function_history.append(self.temporary_solution.cost)
            iterations += 1
            T = self.calculate_temperature(iterations)

    def get_objective_function_history(self) -> float:
        return self.objective_function_history












