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

class SimulatedAnnealing:
    def __init__(self, network: OpticalFibreNetwork) -> None:
        self.empty_network = network
        self.actual_solution = None
        self.best_solution = None


    def create_beginning_solution(self) -> None:
        pass

    def device_neighbourhood(self) -> None:
        pass

    def edge_neighbourhood(self) -> None:
        pass
        
    def check_network_correctness(self, network: OpticalFibreNetwork) -> bool:
        pass

    def run_alghoritm(self) -> None:
        pass