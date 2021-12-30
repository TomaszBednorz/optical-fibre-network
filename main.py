from data_structures import *
from SA import *
import matplotlib.pyplot as plt
import sys


if __name__ == "__main__":
    network = OpticalFibreNetwork()
    network.add_starting_point(50.16429619810853, 19.626773362067187)
    network.add_buildings_from_txt('tests/test1_buildings.txt')
    network.add_poles_from_txt('tests/test1_poles.txt')


    sa_param = SA_parameters()
    sa_param.buildings = True
    sa_param.poles = True
    sa_param.devices = True
    sa_param.max_temperature = 100
    sa_param.max_iterations = 50
    sa_param.max_subiterations = 10
    sa_param.alpha = 100

    sa = SimulatedAnnealing(network,sa_param)
    sa.run_alghoritm()
    sa.best_solution.visualization(True,False) 
    print("Objective function cost: {} zł".format(sa.best_solution.cost))

    simple_sol = sa.best_solution.get_simple_solution()
    print("\nCost: {} zł".format(simple_sol[2]))

    print("\nOptical fibre network:")
    for key, value in simple_sol[0].items():
        print("{} : {}".format(key, value))

    print("\nDevices:")
    for key, value in simple_sol[1].items():
        print("{} : {}".format(key, value))

    history = sa.get_objective_function_history()
    plt.plot(history)
    plt.grid()
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.title("Objective function cost in time")
    plt.show()

    # print("Buildings updates: {}".format(sa.realizations[0]))
    # print("Poles updates: {}".format(sa.realizations[1]))
    # print("Devices updates: {}".format(sa.realizations[2]))

    # iterations = sa_param.max_iterations * sa_param.max_subiterations
    # print("Worse cost (not accepted): {}  {:.3}%".format(sa.quality_changes[0], sa.quality_changes[0]/ iterations))
    # print("Worse cost (accepted): {}  {:.3}%".format(sa.quality_changes[1], sa.quality_changes[1]/ iterations))
    # print("Better cost: {}  {:.3}%".format(sa.quality_changes[2], sa.quality_changes[2]/ iterations))

    # print("Worse cost (not accepted): {}".format(sa.quality_changes_it['worse_not_acepted']))
    # print("Worse cost (accepted): {}".format(sa.quality_changes_it['worse_accepted']))
    # print("Better cost: {}".format(sa.quality_changes_it['better']))

    