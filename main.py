from data_structures import *
from network import *


if __name__ == "__main__":
    network = OpticalFibreNetwork()

    network.add_buildings_from_txt('buildings.txt')
    network.add_poles_from_txt('poles.txt')

    # network.add_device(dev_10)
    # network.add_device(dev_25)

    # network.add_edge(network.buildings[0], network.buildings[1])
    # network.add_edge(network.buildings[1], network.buildings[2])



    network.generate_edges(7)
    network.generate_edges(9017)
    network.generate_edges(12)
    network.generate_edges(9029)
    network.generate_edges(9006)
    network.generate_edges(31)


    network.calculate_objective_function()
    # cost = network.get_cost()
    network.visualization(True)                     # Add as an argument True to display the id's on map
    # print("Objective function cost: {:.8} zł".format(cost))


    network.save_buildings_to_txt('buildings.txt')
    network.save_poles_to_txt('poles.txt')