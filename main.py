from data_structures import *
from network import *
from plotting_data import visualization
from network import list_b, list_p


if __name__ == "__main__":
    optical_fibre_network = Network()
    visualization(list_b,list_p)
    
    # In future
    # visualization(Network.buildings, Network.poles)

    add_poles_to_network(optical_fibre_network)
    add_buildings_to_network(optical_fibre_network)
    add_devices_to_network(optical_fibre_network)
    add_edges_to_network(optical_fibre_network)


    #show_cost


    # 1. Dodać słupy, budynki (niekoniecznie wszystkie)
    # 2. Stworzyć losowe krawędzie (fajnie jakby potem można było to wyświetlić)
    # 3. Wypluć koszt obecnego połączenia