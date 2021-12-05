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
    sa.actual_solution.visualization(True,False)                     # First argument: True to display the id's on map, Secound argument: True to display empty edges


    for key in sa.actual_solution.edges:
        for el in sa.actual_solution.edges[key]:
            dist = el.distance
            a = el.start.id
            b = el.end.id
            ty = el.type
            num = len(el.optical_fibres)
            print("{} : {} dist: {} type: {} len: {}".format(a, b, dist, ty, num))

    print("Objective function cost: {} zł".format(cost))
    sa.empty_network.calculate_objective_function()
    print(sa.empty_network.cost)
    # network.calculate_objective_function()
    # cost = network.get_cost()
    # network.visualization(True)                     # Add as an argument True to display the id's on map
    # print("Objective function cost: {} zł".format(cost))
