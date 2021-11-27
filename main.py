from data_structures import *
from network import *


if __name__ == "__main__":
    optical_fibre_network = Network()


    add_poles_to_network(optical_fibre_network)
    add_buildings_to_network(optical_fibre_network)
    add_devices_to_network(optical_fibre_network)
    add_edges_to_network(optical_fibre_network)


    #show_cost


    # 1. Dodać słupy, budynki (niekoniecznie wszystkie)
    # 2. Stworzyć losowe krawędzie (fajnie jakby potem można było to wyświetlić)
    # 3. Wypluć koszt obecnego połączenia