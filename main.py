from data_structures import *
from network import *
from plotting_data import visualization


if __name__ == "__main__":
    network = OpticalFibreNetwork()

    # visualization(list_of_buildings,list_of_poles)
    
    # In future
    # visualization(Network.buildings, Network.poles)

    for building in list_of_buildings:
        network.add_building(building.vert_coord, building.hori_coord, building.id)

    for pole in list_of_poles:
        network.add_pole(pole.vert_coord, pole.hori_coord, pole.id)


    network.add_device(dev_10)
    network.add_device(dev_25)

    network.add_edge(network.buildings[0], network.buildings[1], of_overhead_3)
    network.add_edge(network.buildings[1], network.buildings[2], of_overhead_3)
    network.add_edge(network.buildings[2], network.buildings[3], of_overhead_3)
    network.add_edge(network.buildings[3], network.buildings[4], of_overhead_3)
    network.add_edge(network.buildings[4], network.buildings[5], of_overhead_3)
    network.add_edge(network.buildings[5], network.buildings[6], of_overhead_2)
    network.add_edge(network.buildings[6], network.buildings[7], of_overhead_2)
    network.add_edge(network.buildings[7], network.buildings[8], of_overhead_2)
    network.add_edge(network.buildings[8], network.buildings[9], of_overhead_2)
    network.add_edge(network.buildings[9], network.buildings[10], of_overhead_2)



    network.calculate_objective_function()

    cost = network.get_cost()
    print("Objective function cost: {:.8} zł".format(cost))
