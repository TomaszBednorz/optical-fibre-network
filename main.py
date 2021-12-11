from data_structures import *
from SA import *
import matplotlib.pyplot as plt


if __name__ == "__main__":
    network = OpticalFibreNetwork()
    network.add_starting_point(50.16429619810853, 19.626773362067187)
    network.add_buildings_from_txt('buildings.txt')
    network.add_poles_from_txt('poles.txt')

    sa = SimulatedAnnealing(network)
    sa.run_alghoritm()
    sa.best_solution.visualization2(True,False) 
    print("Objective function cost: {} zł".format(sa.best_solution.cost))

    history = sa.get_objective_function_history()

    plt.plot(history)
    plt.grid()
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.title("Objective function cost in time")
    plt.show()
    # sol_corect = False

    # while not sol_corect:
    #     sa.create_beginning_solution(25)
    #     sol_corect = sa.check_network_correctness(sa.actual_solution)
        

    # sa.actual_solution.calculate_objective_function()
    # cost = sa.actual_solution.get_cost()
    # sa.actual_solution.visualization(True,False)                     # First argument: True to display the id's on map, Secound argument: True to display empty edges
    # x = sa.check_network_correctness(sa.actual_solution)
    # print(x)

    # for _ in range(1):
    #     for _ in range(300):
    #         sa.temporary_solution = sa.update_node_neighbourhood(4, NodeType.BUILDING)
    #         sa.temporary_solution.calculate_objective_function()
    #         var = sa.check_network_correctness(sa.temporary_solution)
    #         if sa.temporary_solution.cost < cost + 1000 and var:
    #             sa.actual_solution = sa.temporary_solution
    #             cost = sa.actual_solution.cost
    #             print(sa.actual_solution.cost)

    #         sa.temporary_solution = sa.update_node_neighbourhood(4, NodeType.POLE)
    #         sa.temporary_solution.calculate_objective_function()
    #         var = sa.check_network_correctness(sa.temporary_solution)
    #         if sa.temporary_solution.cost < cost + 1000 and var:
    #             sa.actual_solution = sa.temporary_solution
    #             cost = sa.actual_solution.cost
    #             print(sa.actual_solution.cost)
        
    #     for _ in range(300):
    #         sa.temporary_solution = sa.update_node_neighbourhood(4, NodeType.BUILDING)
    #         sa.temporary_solution.calculate_objective_function()
    #         var = sa.check_network_correctness(sa.temporary_solution)
    #         if sa.temporary_solution.cost < cost + 500 and var:
    #             sa.actual_solution = sa.temporary_solution
    #             cost = sa.actual_solution.cost
    #             print(sa.actual_solution.cost)

    #         sa.temporary_solution = sa.update_node_neighbourhood(4, NodeType.POLE)
    #         sa.temporary_solution.calculate_objective_function()
    #         var = sa.check_network_correctness(sa.temporary_solution)
    #         if sa.temporary_solution.cost < cost + 500 and var:
    #             sa.actual_solution = sa.temporary_solution
    #             cost = sa.actual_solution.cost
    #             print(sa.actual_solution.cost)

    #     for _ in range(300):
    #         sa.temporary_solution = sa.update_node_neighbourhood(4, NodeType.BUILDING)
    #         sa.temporary_solution.calculate_objective_function()
    #         var = sa.check_network_correctness(sa.temporary_solution)
    #         if sa.temporary_solution.cost < cost and var:
    #             sa.actual_solution = sa.temporary_solution
    #             cost = sa.actual_solution.cost
    #             print(sa.actual_solution.cost)

    #         sa.temporary_solution = sa.update_node_neighbourhood(4, NodeType.POLE)
    #         sa.temporary_solution.calculate_objective_function()
    #         var = sa.check_network_correctness(sa.temporary_solution)
    #         if sa.temporary_solution.cost < cost and var:
    #             sa.actual_solution = sa.temporary_solution
    #             cost = sa.actual_solution.cost
    #             print(sa.actual_solution.cost)


            
    #     for _ in range(3):
    #         new_sol = sa.update_node_neighbourhood(4, NodeType.BUILDING)
    #         new_sol.calculate_objective_function()
    #         sa.actual_solution = new_sol
    #         cost = sa.actual_solution.cost
    #         print(sa.actual_solution.cost)

    #         new_sol = sa.update_node_neighbourhood(4, NodeType.POLE)
    #         new_sol.calculate_objective_function()
    #         sa.actual_solution = new_sol
    #         cost = sa.actual_solution.cost
    #         print(sa.actual_solution.cost)



    # for key in sa.actual_solution.edges:
    #     for el in sa.actual_solution.edges[key]:
    #         dist = el.distance
    #         a = el.start.id
    #         b = el.end.id
    #         ty = el.type
    #         num = len(el.optical_fibres)
    #         print("{} : {} dist: {} type: {} len: {}".format(a, b, dist, ty, num))

    # amount = 0
    # for node in sa.actual_solution.all_nodes:
    #     for device in node.devices: 
    #         amount += device.amount       
    # print(amount)
    
    # print("Objective function cost: {} zł".format(cost))
    # sa.empty_network.calculate_objective_function()
    # print(sa.empty_network.cost)
    # network.calculate_objective_function()
    # cost = network.get_cost()
    # network.visualization(True)                     # Add as an argument True to display the id's on map
    # print("Objective function cost: {} zł".format(cost))
