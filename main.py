from data_structures import *
from network import *


if __name__ == "__main__":
    network = OpticalFibreNetwork()

    network.add_buildings_from_txt('buildings.txt')
    network.add_poles_from_txt('poles.txt')

    network.add_device(dev_10)
    network.add_device(dev_25)

    network.add_edge(network.buildings[0], network.buildings[1])
    network.add_edge(network.buildings[1], network.buildings[2])
    network.add_edge(network.buildings[2], network.buildings[3])
    network.add_edge(network.buildings[3], network.buildings[4])
    network.add_edge(network.buildings[4], network.buildings[5])
    network.add_edge(network.buildings[5], network.buildings[6])
    network.add_edge(network.buildings[6], network.buildings[7])
    network.add_edge(network.buildings[7], network.buildings[8])
    network.add_edge(network.buildings[8], network.buildings[9])
    network.add_edge(network.buildings[9], network.buildings[10])
    network.add_edge(network.poles[6], network.poles[2])
    network.add_edge(network.poles[8], network.poles[3])
    network.add_edge(network.poles[9], network.poles[3])
    network.add_edge(network.poles[11], network.poles[3])
    network.add_edge(network.poles[5], network.poles[0])




    network.calculate_objective_function()

    cost = network.get_cost()
    network.visualization(True)                     # Add as an argument True to display the id's on map
    print("Objective function cost: {:.8} zł".format(cost))

    network.save_buildings_to_txt('buildings.txt')
    network.save_poles_to_txt('poles.txt')