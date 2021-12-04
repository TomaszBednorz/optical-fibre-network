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
        pass

    def run_alghoritm(self) -> None:
        pass