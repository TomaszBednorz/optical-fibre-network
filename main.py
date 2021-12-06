from numpy import cos
from data_structures import *
from SA import *



if __name__ == "__main__":
    network = OpticalFibreNetwork()
    network.add_starting_point(50.16429619810853, 19.626773362067187)
    network.add_buildings_from_txt('buildings_for_tests.txt')
    network.add_poles_from_txt('poles_for_tests.txt')

    network.add_edge(network.buildings[1], network.buildings[2])
    network.add_edge(network.buildings[3], network.buildings[5])

    sa = SimulatedAnnealing(network)
    sa.create_beginning_solution(50)

    sa.actual_solution.calculate_objective_function()
    cost = sa.actual_solution.get_cost()
    sa.actual_solution.visualization(True)                     # Add as an argument True to display the id's on map

    print("Objective function cost: {} zł".format(cost))

    for i in range(10000):  # Może jak 2 razy wchodzi do tego samego edga/nołda to błąd?

        new_sol = sa.update_node_neighbourhood(2, NodeType.POLE)
        new_sol.calculate_objective_function()
        cost2 = new_sol.get_cost()

        if cost2 < cost:
            sa.actual_solution = new_sol
            cost = cost2
        print(cost)
    
        # new_sol = sa.update_node_neighbourhood(2, NodeType.BUILDING)
        # new_sol.calculate_objective_function()
        # cost3 = new_sol.get_cost()

        # if cost3 <= cost:
        #     sa.actual_solution = new_sol
        # print(cost3)


    # for key in sa.actual_solution.edges:
    #     for el in sa.actual_solution.edges[key]:
    #         dist = el.distance
    #         a = el.start.id
    #         b = el.end.id
    #         ty = el.type
    #         num = len(el.optical_fibres)
    #         print("{} : {} dist: {} type: {} len: {}".format(a, b, dist, ty, num))

    print("Num of devices: {}".format(len(sa.actual_solution.devices)))
    print("Objective function cost: {} zł".format(cost))

    sa.empty_network.calculate_objective_function()
    print(sa.empty_network.cost)
