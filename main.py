from data_structures import *
from SA import *

if __name__ == "__main__":
    network = OpticalFibreNetwork()
    network.add_starting_point(50.16429619810853, 19.626773362067187)
    network.add_buildings_from_txt('buildings_for_tests.txt')
    network.add_poles_from_txt('poles_for_tests.txt')

    sa = SimulatedAnnealing(network)
    sa.create_beginning_solution()

    sa.actual_solution.calculate_objective_function()
    cost = sa.actual_solution.get_cost()
    sa.actual_solution.visualization(True)                     # Add as an argument True to display the id's on map
    print("Objective function cost: {} zł".format(cost))


    # for key in network.edges:
    #     for el in network.edges[key]:
    #         dist = el.distance
    #         a = el.start.id
    #         b = el.end.id
    #         print("{} : {} dist: {}".format(a, b, dist))



    # network.calculate_objective_function()
    # cost = network.get_cost()
    # network.visualization(True)                     # Add as an argument True to display the id's on map
    # print("Objective function cost: {} zł".format(cost))
