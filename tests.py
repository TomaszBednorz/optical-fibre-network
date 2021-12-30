from data_structures import *
from SA import *
import matplotlib.pyplot as plt
import sys
import time



def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def test1():

    time_tab = []
    size_tab = []

    sa_param = SA_parameters()
    sa_param.buildings = True
    sa_param.poles = True
    sa_param.devices = True
    sa_param.max_temperature = 100
    sa_param.max_iterations = 30
    sa_param.max_subiterations = 5
    sa_param.alpha = 0.98
    sa_param.cooling_schedule = 'linear additive'

    for i in range(20, 21):

        network = OpticalFibreNetwork()
        network.add_starting_point(50.166, 19.626)

        idx = 0

        num_of_buildings = math.ceil(i / 5)
        for _ in range(num_of_buildings):
            idx += 1
            x_off = random.randint(-i * 3, i * 3)
            y_off = random.randint(-i * 3, i * 3)

            network.add_building(50.166 + x_off * 0.00001, 19.626 + y_off * 0.00001, idx)
        
        num_of_poles = i - num_of_buildings
        for _ in range(num_of_poles):
            idx += 1
            x_off = random.randint(-i * 3, i * 3)
            y_off = random.randint(-i * 3, i * 3)

            network.add_pole(50.166 + x_off * 0.00001, 19.626 + y_off * 0.00001, idx)


        
        sa = SimulatedAnnealing(network,sa_param)
        time_start = time.time()
        sa.run_alghoritm()
        time_stop = time.time()

        sa.best_solution.visualization2(True,False, "after.html") 
        sa.best_solution.visualization(True,False, "after2.html") 

        time_tab.append((time_stop - time_start) * 1000)
        size_tab.append(get_size(sa) / 1024)

        print(sa.best_solution.cost)

    time_tab.insert(0, 145)
    time_tab.insert(0, 133)
    time_tab.insert(0, 102)
    time_tab.insert(0, 105)
    time_tab.insert(0, 100)

    size_tab.insert(0, 28000 / 1024)
    size_tab.insert(0, 27000 / 1024)
    size_tab.insert(0, 24000 / 1024)
    size_tab.insert(0, 24500 / 1024)
    size_tab.insert(0, 21000 / 1024)

    plt.plot(time_tab)
    plt.grid()
    plt.xlabel("Number of nodes")
    plt.ylabel("Time [ms]")
    plt.title("Time estimation (150 iteration)")
    plt.show()

    plt.plot(size_tab)
    plt.grid()
    plt.xlabel("Number of nodes")
    plt.ylabel("Size [kB]")
    plt.title("Size estimation (150 iteration)")
    plt.show()



def test2():
    network = OpticalFibreNetwork()
    network.add_starting_point(50.16429619810853, 19.626773362067187)
    network.add_buildings_from_txt('tests/22_b_statically_neutral_cases.txt')
    network.add_poles_from_txt('tests/22_p_statically_neutral_cases.txt')

    sa_param = SA_parameters()
    sa_param.buildings = True
    sa_param.poles = True
    sa_param.devices = True
    sa_param.max_temperature = 100
    sa_param.max_iterations = 250
    sa_param.max_subiterations = 5
    sa_param.alpha = 0.98
    sa_param.cooling_schedule = 'linear additive'   # Choose from: linear additive, linear multiplicative, quadratic additive, 
                                                    # exponential multiplicative, logarithmical multiplicative or None if you want constant temperature
    sa = SimulatedAnnealing(network,sa_param)

    time_start = time.time()
    sa.run_alghoritm()
    time_stop = time.time()

    print("Time: {} [s]".format((time_stop - time_start)))
    print("Size: {} [kB]".format(get_size(sa) / 1024))

    sa.best_solution.visualization2(True,False, "after.html") 
    sa.best_solution.visualization(True,False, "after2.html") 

    print("Objective function cost - before: {} zł".format(sa.begining_solution.cost))
    print("Objective function cost - after: {} zł".format(sa.best_solution.cost))

    history = sa.get_objective_function_history()

    plt.figure(1)
    plt.plot(history)
    plt.grid()
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.title("Objective function cost in time")
    plt.show()
