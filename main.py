from data_structures import *
from SA import *
import matplotlib.pyplot as plt


if __name__ == "__main__":
    network = OpticalFibreNetwork()
    network.add_starting_point(50.16429619810853, 19.626773362067187)
    network.add_buildings_from_txt('buildings.txt')
    network.add_poles_from_txt('poles.txt')


    sa_param = SA_parameters()
    sa_param.buildings = True
    sa_param.poles = True
    sa_param.devices = True
    sa_param.max_temperature = 100
    sa_param.max_iterations = 100
    sa_param.max_subiterations = 10
    sa_param.alpha = 100

    sa = SimulatedAnnealing(network,sa_param)
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
